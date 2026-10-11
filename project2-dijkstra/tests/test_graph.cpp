#include "examples.hpp"
#include "test_support.hpp"
#include <functional>

int main() {
    return run_test("shared graph conversion and validation", [] {
        using namespace project2;
        const auto edges = teaching_graph();
        const auto matrix = make_matrix(edges);
        const auto list = make_list(edges);
        require(matrix.vertex_count == 5 && list.vertex_count == 5, "Vertex count");
        std::size_t entries = 0;
        for (Vertex u = 0; u < 5; ++u) {
            require(matrix.weights[u][u] == 0, "Diagonal");
            for (const auto& neighbor : list.neighbors[u]) {
                require(matrix.weights[u][neighbor.vertex] == neighbor.weight,
                        "Representation mismatch");
                ++entries;
            }
        }
        require(entries == 14, "Undirected list entry count");
        for (const auto& edge : edges.edges) {
            require(matrix.weights[edge.u][edge.v] == edge.weight &&
                    matrix.weights[edge.v][edge.u] == edge.weight, "Edge symmetry");
        }
        require(matrix.weights[0][4] == kInfinity, "Absent edge");
        const auto zero = make_matrix({3, {{0, 1, 0}}});
        require(zero.weights[0][1] == 0 && zero.weights[0][2] == kInfinity,
                "Zero edge versus absence");
        require(make_list({1, {}}).neighbors[0].empty(), "Single vertex");
        auto rejects = [](const EdgeListGraph& invalid) {
            for (bool as_matrix : {false, true}) {
                bool rejected = false;
                try {
                    if (as_matrix) (void)make_matrix(invalid);
                    else (void)make_list(invalid);
                } catch (const std::invalid_argument&) { rejected = true; }
                require(rejected, "Invalid graph accepted");
            }
        };
        rejects({0, {}});
        rejects({2, {{0, 0, 1}}});
        rejects({2, {{1, 0, 1}}});
        rejects({2, {{0, 2, 1}}});
        rejects({2, {{0, 1, -1}}});
        rejects({2, {{0, 1, kInfinity}}});
        rejects({2, {{0, 1, 1}, {0, 1, 2}}});
        rejects({4, {{0, 1, kInfinity / 2}}});
    });
}
