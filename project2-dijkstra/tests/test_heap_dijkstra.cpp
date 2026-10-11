#include "dijkstra.hpp"
#include "examples.hpp"
#include "test_support.hpp"

int main() {
    return run_test("Member B list Dijkstra acceptance cases", [] {
        using namespace project2;
        OperationStats stats{};
        const auto result = dijkstra_heap(make_list(teaching_graph()), 0, &stats);
        require(result.distances == teaching_distances(), "Teaching distances");
        require(result.parents.size() == 5 && result.parents[0] == kNoVertex,
                "Source parent");
        require(stats.adjacency_entries_scanned == 14 && stats.heap_inserts == 5 &&
                stats.heap_extracts == 5 && stats.heap_decreases == 3, "Heap counters");
        require(dijkstra_heap(make_list({3, {{0, 1, 2}}}), 0).distances ==
                std::vector<Distance>({0, 2, kInfinity}), "Unreachable vertex");
        require(dijkstra_heap(make_list({3, {{0, 1, 0}, {1, 2, 0}, {0, 2, 5}}}), 0)
                .distances == std::vector<Distance>({0, 0, 0}), "Zero-weight path");
        require(dijkstra_heap(make_list({1, {}}), 0).distances ==
                std::vector<Distance>({0}), "Single vertex");
        // Member B: extend with other sources, invalid source, equal paths,
        // large weights and predecessor validation before handing off to C.
    });
}
