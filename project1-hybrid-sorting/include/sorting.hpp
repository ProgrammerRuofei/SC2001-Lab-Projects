#pragma once

#include <cstdint>
#include <vector>

namespace sc2001 {

using ComparisonCount = std::int64_t;

// All ranges use inclusive boundaries: [left, right].
// TODO(student): Implement these algorithms in src/sorting.cpp.
void insertionSort(std::vector<int>& values,
                   int left,
                   int right,
                   ComparisonCount& keyComparisons);

void merge(std::vector<int>& values,
           int left,
           int middle,
           int right,
           ComparisonCount& keyComparisons);

void mergeSort(std::vector<int>& values,
               int left,
               int right,
               ComparisonCount& keyComparisons);

void hybridMergeSort(std::vector<int>& values,
                     int left,
                     int right,
                     int threshold,
                     ComparisonCount& keyComparisons);

}  // namespace sc2001

