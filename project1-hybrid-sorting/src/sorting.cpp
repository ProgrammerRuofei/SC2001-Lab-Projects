#include "sorting.hpp"

namespace sc2001 {

void insertionSort(std::vector<int>& values,
                   int left,
                   int right,
                   ComparisonCount& keyComparisons) {
    // Empty and single-element ranges are already sorted.
    if (left >= right) {
        return;
    }

    for (int i = left + 1; i <= right; ++i) {
        // values[left..i-1] is sorted; insert the saved key into that prefix.
        const int key = values[i];
        int j = i - 1;

        while (j >= left) {
            // Count every key comparison, including one that stops shifting.
            ++keyComparisons;
            if (values[j] <= key) {
                break;
            }
            values[j + 1] = values[j];
            --j;
        }

        values[j + 1] = key;
    }
}

// TODO(student): Implement the two-pointer merge operation here.

// TODO(student): Implement original Merge Sort here.

// TODO(student): Implement Hybrid Merge Sort here after the earlier algorithms
// have been implemented and tested.

}  // namespace sc2001
