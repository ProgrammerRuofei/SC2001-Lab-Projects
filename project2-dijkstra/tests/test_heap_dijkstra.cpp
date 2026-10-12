#include "dijkstra.hpp"
#include "examples.hpp"
#include "test_support.hpp"

#include <random>
#include <stdexcept>

namespace {
using namespace project2;

// Independent edge-list Bellman-Ford oracle, confined to Role B's test file.
std::vector<Distance> reference(const EdgeListGraph& graph, Vertex source) {
    std::vector<Distance> dist(graph.vertex_count, kInfinity);
    dist[source] = 0;
    for (Vertex round = 1; round < graph.vertex_count; ++round) {
        bool changed = false;
        for (const auto& e : graph.edges) {
            auto relax = [&](Vertex u, Vertex v) {
                if (dist[u] == kInfinity || e.weight >= kInfinity - dist[u]) return;
                const auto candidate = dist[u] + e.weight;
                if (candidate < dist[v]) { dist[v] = candidate; changed = true; }
            };
            relax(e.u, e.v);
            relax(e.v, e.u);
        }
        if (!changed) break;
    }
    return dist;
}

void validate_paths(const ListGraph& graph, Vertex source, const DijkstraResult& result) {
    require(result.distances.size() == graph.vertex_count &&
            result.parents.size() == graph.vertex_count, "Result sizes");
    require(result.distances[source] == 0 && result.parents[source] == kNoVertex,
            "Source result");
    for (Vertex v = 0; v < graph.vertex_count; ++v) {
        if (result.distances[v] == kInfinity) {
            require(result.parents[v] == kNoVertex, "Unreachable parent");
            continue;
        }
        Vertex current = v;
        Distance total = 0;
        Vertex steps = 0;
        while (current != source) {
            require(++steps < graph.vertex_count, "No parent cycle");
            const auto parent = result.parents[current];
            require(parent < graph.vertex_count, "Valid predecessor");
            bool found = false;
            for (const auto& neighbor : graph.neighbors[parent]) {
                if (neighbor.vertex != current) continue;
                require(neighbor.weight < kInfinity - total, "Safe path sum");
                total += neighbor.weight;
                found = true;
                break;
            }
            require(found, "Predecessor edge exists");
            current = parent;
        }
        require(total == result.distances[v], "Path weight matches distance");
    }
}

DijkstraResult check(const EdgeListGraph& edges, Vertex source) {
    const auto graph = make_list(edges);
    const auto result = dijkstra_heap(graph, source);
    require(result.distances == reference(edges, source), "Independent distances");
    validate_paths(graph, source, result);
    return result;
}
}

int main() {
    return run_test("Member B list Dijkstra acceptance cases", [] {
        using namespace project2;
        const auto graph = make_list(teaching_graph());
        OperationStats stats{};
        const auto result = dijkstra_heap(graph, 0, &stats);
        require(result.distances == teaching_distances(), "Teaching distances");
        validate_paths(graph, 0, result);
        require(stats.adjacency_entries_scanned == 14 && stats.heap_inserts == 5 &&
                stats.heap_extracts == 5 && stats.heap_decreases == 3 &&
                stats.relax_attempts == 7 && stats.relax_successes == 7,
                "Teaching counters");
        require(stats.min_scan_slots == 0 && stats.matrix_scan_slots == 0,
                "Matrix counters untouched");
        require(dijkstra_heap(graph, 0).distances == result.distances,
                "Counter-disabled results");
        for (Vertex source = 0; source < 5; ++source) check(teaching_graph(), source);
        const auto unreachable = check({3, {{0, 1, 2}}}, 0);
        require(unreachable.distances == std::vector<Distance>({0, 2, kInfinity}),
                "Unreachable vertex");
        check({4, {}}, 2);
        require(check({2, {{0, 1, 5}}}, 0).distances ==
                std::vector<Distance>({0, 5}), "One edge");
        require(check({2, {{0, 1, 5}}}, 1).distances ==
                std::vector<Distance>({5, 0}), "Other source");
        require(check({3, {{0, 1, 10}, {0, 2, 1}, {1, 2, 1}}}, 0).distances ==
                std::vector<Distance>({0, 2, 1}), "Indirect shorter route");
        require(check({3, {{1, 2, 4}}}, 0).distances ==
                std::vector<Distance>({0, kInfinity, kInfinity}), "Isolated source");
        check({3, {{0, 1, 0}, {1, 2, 0}, {0, 2, 5}}}, 0);
        check({4, {{0, 1, 0}, {0, 2, 0}, {1, 2, 0}, {1, 3, 1}, {2, 3, 1}}}, 0);
        const auto equal = check({4, {{0, 1, 1}, {0, 2, 1}, {1, 3, 1}, {2, 3, 1}}}, 0);
        require(equal.parents[3] == 1, "Tie order and strict updates");
        check({1, {}}, 0);
        const Weight large = (kInfinity - 1) / 2;
        require(check({3, {{0, 1, large}, {1, 2, large}}}, 0).distances[2] ==
                2 * large, "Large finite distance");
        require(check({2, {{0, 1, kInfinity - 1}}}, 0).distances[1] ==
                kInfinity - 1, "Distance just below INF");
        for (const auto& invalid : {ListGraph{0, {}}, graph}) {
            bool caught = false;
            try { dijkstra_heap(invalid, invalid.vertex_count); }
            catch (const std::invalid_argument&) { caught = true; }
            require(caught, "Invalid source rejected");
        }

        std::mt19937 rng(2001);
        for (int trial = 0; trial < 250; ++trial) {
            const Vertex n = 2 + rng() % 29;
            const unsigned density_percent = static_cast<unsigned>(trial % 5) * 25;
            EdgeListGraph edges{n, {}};
            for (Vertex u = 0; u < n; ++u)
                for (Vertex v = u + 1; v < n; ++v)
                    if (rng() % 100 < density_percent)
                        edges.edges.push_back({u, v, rng() % 21});
            const Vertex source = rng() % n;
            const auto expected = check(edges, source);
            OperationStats counts{};
            const auto counted = dijkstra_heap(make_list(edges), source, &counts);
            require(counted.distances == expected.distances &&
                    counted.parents == expected.parents, "Counters preserve results");
            std::uint64_t reachable = 0, scans = 0, attempts = 0;
            for (const auto distance : expected.distances)
                if (distance != kInfinity) ++reachable;
            for (const auto& edge : edges.edges) {
                if (expected.distances[edge.u] == kInfinity) continue;
                scans += 2;
                ++attempts;
            }
            require(counts.heap_inserts == reachable && counts.heap_extracts == reachable &&
                    counts.adjacency_entries_scanned == scans &&
                    counts.relax_attempts == attempts &&
                    counts.relax_successes == reachable - 1 + counts.heap_decreases &&
                    counts.min_scan_slots == 0 && counts.matrix_scan_slots == 0,
                    "Reachable-component counter invariants");
        }
    });
}
