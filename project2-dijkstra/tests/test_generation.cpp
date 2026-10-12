#include "generation.hpp"
#include "dijkstra.hpp"
#include "test_support.hpp"

#include <algorithm>
#include <limits>
#include <queue>
#include <set>
#include <utility>

namespace {
using namespace project2;

void validate(const GraphSpec& spec, const EdgeListGraph& graph) {
    require(graph.vertex_count == spec.vertex_count && graph.edges.size() == spec.edge_count,
            "Exact n/m");
    std::vector<std::vector<Vertex>> neighbors(spec.vertex_count);
    std::set<std::pair<Vertex, Vertex>> seen;
    std::pair<Vertex, Vertex> previous{0, 0};
    bool first = true;
    for (const auto& edge : graph.edges) {
        require(edge.u < edge.v && edge.v < spec.vertex_count, "Canonical valid IDs");
        const auto pair = std::make_pair(edge.u, edge.v);
        require(seen.insert(pair).second, "Unique logical edges");
        require(first || previous < pair, "Sorted edges");
        previous = pair; first = false;
        require(edge.weight >= spec.weight_min && edge.weight <= spec.weight_max,
                "Weight range");
        neighbors[edge.u].push_back(edge.v);
        neighbors[edge.v].push_back(edge.u);
    }
    // Check connectivity directly from the raw edge set, independently of Dijkstra.
    std::vector<bool> visited(spec.vertex_count, false);
    std::queue<Vertex> queue;
    visited[0] = true; queue.push(0);
    std::size_t reached = 0;
    while (!queue.empty()) {
        const auto u = queue.front(); queue.pop(); ++reached;
        for (const auto v : neighbors[u]) {
            if (visited[v]) continue;
            visited[v] = true; queue.push(v);
        }
    }
    require(reached == spec.vertex_count, "Connected input");
    const auto matrix = make_matrix(graph);
    const auto list = make_list(graph);
    std::size_t entries = 0;
    for (Vertex u = 0; u < spec.vertex_count; ++u) {
        require(matrix.weights[u][u] == 0, "Matrix diagonal");
        for (const auto& neighbor : list.neighbors[u]) {
            ++entries;
            require(matrix.weights[u][neighbor.vertex] == neighbor.weight,
                    "Representation weights agree");
        }
    }
    require(entries == 2 * spec.edge_count, "Two list entries per logical edge");
    for (const auto source : {Vertex{0}, spec.vertex_count - 1}) {
        const auto a = dijkstra_matrix(matrix, source);
        const auto b = dijkstra_heap(list, source);
        require(a.distances == b.distances && a.parents == b.parents,
                "Generated input works in both algorithms");
        for (const auto distance : a.distances)
            require(distance != kInfinity, "All generated vertices are reachable");
    }
}

void check(const GraphSpec& spec) {
    const auto graph = generate_connected_graph(spec);
    validate(spec, graph);
    const auto again = generate_connected_graph(spec);
    require(graph.edges.size() == again.edges.size(), "Reproducible size");
    for (std::size_t i = 0; i < graph.edges.size(); ++i) {
        const auto& a = graph.edges[i]; const auto& b = again.edges[i];
        require(a.u == b.u && a.v == b.v && a.weight == b.weight,
                "Seed reproduces topology and weights");
    }
}

void rejects(const GraphSpec& spec) {
    bool caught = false;
    try { (void)generate_connected_graph(spec); }
    catch (const std::invalid_argument&) { caught = true; }
    require(caught, "Invalid generator parameter rejected");
}
}  // namespace

int main() {
    return run_test("Member C connected graph generator", [] {
        check({20, 80, 2001, 1, 1000});
        check({1, 0, 2001, 0, 0});
        check({2, 1, 0, kInfinity - 1, kInfinity - 1});
        check({3, 3, 2001, kInfinity / 2, kInfinity / 2});
        // Every feasible edge count exercises minimum trees, branch boundaries,
        // dense and complete graphs. Include zero and maximum uint64 seeds.
        for (Vertex n = 2; n <= 12; ++n) {
            const auto capacity = n * (n - 1) / 2;
            for (std::size_t m = n - 1; m <= capacity; ++m)
                for (const auto seed : {std::uint64_t{0}, std::uint64_t{2001},
                                       std::numeric_limits<std::uint64_t>::max()})
                    check({n, m, seed, 0, 20});
        }
        check({100, 99, 42, 7, 7});
        check({100, 400, 2001, 1, 1000});
        check({100, 2475, 2001, 1, 1000});
        check({100, 4950, 2001, 1, 1000});
        rejects({0, 0, 1, 1, 1000});
        rejects({1, 1, 1, 1, 1000});
        rejects({5, 3, 1, 1, 1000});
        rejects({5, 11, 1, 1, 1000});
        rejects({5, 4, 1, -1, 20});
        rejects({5, 4, 1, 10, 9});
        rejects({5, 4, 1, 0, kInfinity});
        rejects({3, 2, 1, 0, (kInfinity + 1) / 2});
        rejects({std::numeric_limits<Vertex>::max(), 0, 1, 0, 0});
    });
}
