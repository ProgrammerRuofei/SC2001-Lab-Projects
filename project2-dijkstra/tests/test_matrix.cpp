#include "dijkstra.hpp"
#include "examples.hpp"
#include "test_support.hpp"

#include <array>
#include <random>
#include <stdexcept>
#include <utility>

namespace {
using namespace project2;

// An independent all-pairs oracle; no Dijkstra selection or heap is reused.
std::vector<std::vector<Distance>> floyd_warshall(const EdgeListGraph& edges) {
    const auto n = edges.vertex_count;
    std::vector<std::vector<Distance>> distances(n, std::vector<Distance>(n, kInfinity));
    for (Vertex v = 0; v < n; ++v) distances[v][v] = 0;
    for (const auto& edge : edges.edges) {
        distances[edge.u][edge.v] = edge.weight;
        distances[edge.v][edge.u] = edge.weight;
    }
    for (Vertex k = 0; k < n; ++k)
        for (Vertex u = 0; u < n; ++u)
            for (Vertex v = 0; v < n; ++v) {
                if (distances[u][k] == kInfinity || distances[k][v] == kInfinity ||
                    distances[k][v] >= kInfinity - distances[u][k]) continue;
                const auto candidate = distances[u][k] + distances[k][v];
                if (candidate < distances[u][v]) distances[u][v] = candidate;
            }
    return distances;
}

void validate_paths(const MatrixGraph& graph, Vertex source, const DijkstraResult& result) {
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
        Vertex steps = 0;
        Distance total = 0;
        while (current != source) {
            require(++steps < graph.vertex_count, "No predecessor cycle");
            const auto parent = result.parents[current];
            require(parent < graph.vertex_count, "Valid predecessor ID");
            const auto weight = graph.weights[parent][current];
            require(weight != kInfinity && weight < kInfinity - total,
                    "Existing edge and safe path sum");
            total += weight;
            current = parent;
        }
        require(total == result.distances[v], "Path weight matches distance");
    }
}

DijkstraResult check(const EdgeListGraph& edges, Vertex source,
                     const std::vector<Distance>& expected) {
    const auto graph = make_matrix(edges);
    OperationStats counts{};
    const auto result = dijkstra_matrix(graph, source, &counts);
    require(result.distances == expected, "Independent shortest distances");
    validate_paths(graph, source, result);
    const auto uncounted = dijkstra_matrix(graph, source);
    require(uncounted.distances == result.distances && uncounted.parents == result.parents,
            "Counters preserve results");
    const auto heap = dijkstra_heap(make_list(edges), source);
    require(heap.distances == result.distances && heap.parents == result.parents,
            "Matrix/heap agreement under the shared tie-breaking contract");
    std::uint64_t reachable = 0, attempts = 0;
    for (const auto distance : expected) if (distance != kInfinity) ++reachable;
    for (const auto& edge : edges.edges)
        if (expected[edge.u] != kInfinity) ++attempts;
    const std::uint64_t rounds = reachable + (reachable < edges.vertex_count ? 1 : 0);
    require(counts.min_scan_slots == rounds * edges.vertex_count &&
            counts.matrix_scan_slots == reachable * edges.vertex_count,
            "Complete scan counts, including final unreachable selection");
    require(counts.relax_attempts == attempts &&
            counts.relax_successes >= reachable - 1 &&
            counts.relax_successes <= counts.relax_attempts, "Relaxation bounds");
    require(counts.heap_inserts == 0 && counts.heap_extracts == 0 &&
            counts.heap_decreases == 0 && counts.adjacency_entries_scanned == 0,
            "Heap/list counters untouched");
    return result;
}

DijkstraResult check(const EdgeListGraph& edges, Vertex source) {
    return check(edges, source, floyd_warshall(edges)[source]);
}
}  // namespace

int main() {
    return run_test("Member A matrix acceptance cases", [] {
        using namespace project2;
        OperationStats stats{};
        const auto result = dijkstra_matrix(make_matrix(teaching_graph()), 0, &stats);
        require(result.distances == teaching_distances(), "Teaching distances");
        require(result.parents.size() == 5 && result.parents[0] == kNoVertex,
                "Source parent");
        require(stats.min_scan_slots == 25 && stats.matrix_scan_slots == 25,
                "Full-scan counts");
        require(dijkstra_matrix(make_matrix({3, {{0, 1, 2}}}), 0).distances ==
                std::vector<Distance>({0, 2, kInfinity}), "Unreachable vertex");
        require(dijkstra_matrix(make_matrix({3, {{0, 1, 0}, {1, 2, 0}, {0, 2, 5}}}), 0)
                .distances == std::vector<Distance>({0, 0, 0}), "Zero-weight path");
        require(dijkstra_matrix(make_matrix({1, {}}), 0).distances ==
                std::vector<Distance>({0}), "Single vertex");
        require(stats.relax_attempts == 7 && stats.relax_successes == 7,
                "Teaching relaxation counters");
        for (Vertex source = 0; source < 5; ++source) check(teaching_graph(), source);
        check({1, {}}, 0);
        check({4, {}}, 2);
        check({2, {{0, 1, 5}}}, 0);
        check({2, {{0, 1, 5}}}, 1);
        check({3, {{0, 1, 2}}}, 0);
        check({3, {{1, 2, 4}}}, 0);
        check({3, {{0, 1, 10}, {0, 2, 1}, {1, 2, 1}}}, 0);
        check({3, {{0, 1, 0}, {1, 2, 0}, {0, 2, 5}}}, 0);
        check({4, {{0, 1, 0}, {0, 2, 0}, {1, 2, 0}, {1, 3, 1}, {2, 3, 1}}}, 0);
        const auto equal = check({4, {{0, 1, 1}, {0, 2, 1}, {1, 3, 1}, {2, 3, 1}}}, 0);
        require(equal.parents[3] == 1, "Vertex-ID tie order and strict updates");
        const Weight large = (kInfinity - 1) / 2;
        require(check({3, {{0, 1, large}, {1, 2, large}}}, 0).distances[2] ==
                2 * large, "64-bit finite distance");
        require(check({2, {{0, 1, kInfinity - 1}}}, 0).distances[1] ==
                kInfinity - 1, "Distance just below INF");
        for (const auto& invalid : {MatrixGraph{0, {}}, make_matrix(teaching_graph())}) {
            bool caught = false;
            try { (void)dijkstra_matrix(invalid, invalid.vertex_count); }
            catch (const std::invalid_argument&) { caught = true; }
            require(caught, "Invalid source rejected");
        }

        // Exhaust all absent/zero/positive edge assignments for four vertices.
        const std::array<std::pair<Vertex, Vertex>, 6> pairs{{
            {0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}}};
        for (unsigned encoding = 0; encoding < 729; ++encoding) {
            EdgeListGraph edges{4, {}};
            unsigned digits = encoding;
            for (const auto& pair : pairs) {
                const auto state = digits % 3;
                digits /= 3;
                if (state) edges.edges.push_back({pair.first, pair.second, state == 1 ? 0 : 2});
            }
            const auto expected = floyd_warshall(edges);
            for (Vertex source = 0; source < 4; ++source) check(edges, source, expected[source]);
        }

        // Use a different seed and oracle from Member B's random tests.
        std::mt19937 rng(2012);
        for (int trial = 0; trial < 250; ++trial) {
            const Vertex n = 2 + rng() % 29;
            const unsigned density_percent = static_cast<unsigned>(trial % 5) * 25;
            EdgeListGraph edges{n, {}};
            for (Vertex u = 0; u < n; ++u)
                for (Vertex v = u + 1; v < n; ++v)
                    if (rng() % 100 < density_percent)
                        edges.edges.push_back({u, v, static_cast<Weight>(rng() % 21)});
            const auto expected = floyd_warshall(edges);
            for (Vertex source = 0; source < n; ++source) check(edges, source, expected[source]);
        }
    });
}
