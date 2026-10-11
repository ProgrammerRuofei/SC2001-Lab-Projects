#include "generation.hpp"
#include "test_support.hpp"

int main() {
    return run_test("Member C generator acceptance cases", [] {
        using namespace project2;
        const auto graph = generate_connected_graph({20, 80, 2001, 1, 1000});
        require(graph.vertex_count == 20 && graph.edges.size() == 80, "Exact n/m");
        (void)make_matrix(graph);
        (void)make_list(graph);
        const auto again = generate_connected_graph({20, 80, 2001, 1, 1000});
        require(graph.edges.size() == again.edges.size(), "Reproducible size");
        for (std::size_t i = 0; i < graph.edges.size(); ++i) {
            const auto& a = graph.edges[i]; const auto& b = again.edges[i];
            require(a.u == b.u && a.v == b.v && a.weight == b.weight,
                    "Seed reproducibility");
            require(a.weight >= 1 && a.weight <= 1000, "Weight range");
        }
        // Member C: add independent BFS/DFS connectivity and invalid parameter cases.
    });
}
