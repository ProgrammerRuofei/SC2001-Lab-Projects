#include "min_heap.hpp"
#include "test_support.hpp"

int main() {
    return run_test("Member B heap acceptance cases", [] {
        using namespace project2;
        IndexedMinHeap heap(5);
        require(heap.empty(), "Initially empty");
        heap.push_or_decrease(2, 9);
        heap.push_or_decrease(1, 4);
        heap.push_or_decrease(3, 4);
        heap.push_or_decrease(2, 1);
        require(heap.size() == 3, "Decrease must not duplicate entries");
        auto first = heap.extract_min();
        require(first.vertex == 2 && first.key == 1 && !heap.contains(2),
                "Decrease and extraction");
        require(heap.extract_min().vertex == 1, "Vertex-ID tie break");
        require(heap.extract_min().vertex == 3 && heap.empty(), "Final extraction");
        // Member B: add no-op updates, invalid/empty operations, more positions,
        // and randomized actions against a linear-scan reference.
    });
}
