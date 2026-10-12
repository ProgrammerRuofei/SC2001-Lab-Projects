#include "min_heap.hpp"
#include "test_support.hpp"

#include <random>
#include <vector>

namespace {
template<class Exception, class Function>
void expect_throw(Function action) {
    bool caught = false;
    try { action(); } catch (const Exception&) { caught = true; }
    require(caught, "Expected exception");
}
}

int main() {
    return run_test("Member B heap acceptance cases", [] {
        using namespace project2;
        IndexedMinHeap heap(5);
        require(heap.empty(), "Initially empty");
        heap.push_or_decrease(2, 9);
        heap.push_or_decrease(1, 4);
        heap.push_or_decrease(3, 4);
        heap.push_or_decrease(2, 1);
        heap.push_or_decrease(2, 1);
        heap.push_or_decrease(2, 8);
        require(heap.size() == 3, "Updates must not duplicate entries");
        auto first = heap.extract_min();
        require(first.vertex == 2 && first.key == 1 && !heap.contains(2),
                "Decrease and extraction");
        require(heap.extract_min().vertex == 1, "Vertex-ID tie break");
        require(heap.extract_min().vertex == 3 && heap.empty(), "Final extraction");
        expect_throw<std::out_of_range>([&] { heap.extract_min(); });
        expect_throw<std::invalid_argument>([&] { heap.contains(5); });
        expect_throw<std::invalid_argument>([&] { heap.push_or_decrease(5, 0); });
        expect_throw<std::invalid_argument>([&] { heap.push_or_decrease(0, -1); });
        expect_throw<std::invalid_argument>([&] { heap.push_or_decrease(0, kInfinity); });
        require(heap.empty(), "Rejected updates preserve state");
        heap.push_or_decrease(2, kInfinity - 1);
        require(heap.extract_min().key == kInfinity - 1, "Largest valid key");
        IndexedMinHeap zero(0);
        expect_throw<std::out_of_range>([&] { zero.extract_min(); });
        expect_throw<std::invalid_argument>([&] { zero.push_or_decrease(0, 0); });

        // Exercise swaps, repeated decreases and reinsertion against a scan oracle.
        constexpr Vertex n = 64;
        IndexedMinHeap random_heap(n);
        std::vector<Distance> keys(n, kInfinity);
        std::mt19937 rng(2001);
        auto check_extract = [&] {
            Vertex best = kNoVertex;
            for (Vertex v = 0; v < n; ++v)
                if (keys[v] != kInfinity &&
                    (best == kNoVertex || keys[v] < keys[best])) best = v;
            require(best != kNoVertex, "Oracle has an entry");
            const auto entry = random_heap.extract_min();
            require(entry.vertex == best && entry.key == keys[best], "Oracle minimum");
            keys[best] = kInfinity;
        };
        for (int step = 0; step < 10000; ++step) {
            if (!random_heap.empty() && rng() % 3 == 0) check_extract();
            else {
                const Vertex v = rng() % n;
                const Distance key = rng() % 1000;
                random_heap.push_or_decrease(v, key);
                if (key < keys[v]) keys[v] = key;
            }
            std::size_t count = 0;
            for (Vertex v = 0; v < n; ++v) {
                const bool present = keys[v] != kInfinity;
                require(random_heap.contains(v) == present, "Position membership");
                if (present) ++count;
            }
            require(random_heap.size() == count && random_heap.empty() == (count == 0),
                    "Oracle size");
        }
        while (!random_heap.empty()) check_extract();
    });
}
