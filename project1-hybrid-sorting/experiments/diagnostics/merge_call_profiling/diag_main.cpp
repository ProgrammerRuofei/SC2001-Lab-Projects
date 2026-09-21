// Diagnostic-only driver: not part of the submitted src/main.cpp.
// Runs one sort and prints key_comparisons, cpu_seconds (instrumented,
// NOT comparable to the formal Part (d) timing), merge_call_count, and
// heap allocation counts/bytes from the global operator new/delete
// overrides in alloc_counters.cpp.

#include "input.hpp"
#include "sorting.hpp"

#include <algorithm>
#include <cstdint>
#include <ctime>
#include <iostream>
#include <stdexcept>
#include <string>

extern long long gNewCalls;
extern long long gDeleteCalls;
extern long long gBytesAllocated;

int main(int argc, char* argv[]) {
    if (argc != 5) {
        std::cerr << "Usage: " << argv[0]
                   << " <hybrid|merge> <n> <S> <seed>\n";
        return 1;
    }

    const std::string algorithm = argv[1];
    const std::size_t n = static_cast<std::size_t>(std::stoll(argv[2]));
    const int threshold = std::stoi(argv[3]);
    const std::uint32_t seed = static_cast<std::uint32_t>(std::stoul(argv[4]));
    const int maxValue = static_cast<int>(n);

    const std::vector<int> originalValues =
        sc2001::generateRandomInput(n, maxValue, seed);

    std::vector<int> values = originalValues;
    sc2001::ComparisonCount keyComparisons = 0;
    sc2001::mergeCallCount = 0;
    const long long newCallsBefore = gNewCalls;
    const long long deleteCallsBefore = gDeleteCalls;
    const long long bytesBefore = gBytesAllocated;

    const std::clock_t start = std::clock();
    if (algorithm == "hybrid") {
        sc2001::hybridMergeSort(
            values, 0, static_cast<int>(values.size()) - 1, threshold,
            keyComparisons
        );
    } else if (algorithm == "merge") {
        sc2001::mergeSort(
            values, 0, static_cast<int>(values.size()) - 1, keyComparisons
        );
    } else {
        throw std::invalid_argument("algorithm must be hybrid or merge");
    }
    const std::clock_t finish = std::clock();

    if (!std::is_sorted(values.begin(), values.end())) {
        throw std::runtime_error("sorting correctness check failed");
    }

    const double cpuSeconds =
        static_cast<double>(finish - start) / CLOCKS_PER_SEC;
    const long long newCalls = gNewCalls - newCallsBefore;
    const long long deleteCalls = gDeleteCalls - deleteCallsBefore;
    const long long bytesAllocated = gBytesAllocated - bytesBefore;

    std::cout
        << algorithm << ','
        << n << ','
        << (algorithm == "hybrid" ? threshold : 0) << ','
        << seed << ','
        << keyComparisons << ','
        << cpuSeconds << ','
        << sc2001::mergeCallCount << ','
        << newCalls << ','
        << deleteCalls << ','
        << bytesAllocated << '\n';

    return 0;
}
