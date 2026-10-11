#include "dijkstra.hpp"
#include "examples.hpp"
#include "test_support.hpp"

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
        // Member A: add equal paths, other sources, invalid source, large weights,
        // and predecessor-path validation from docs/correctness-plan.md.
    });
}
