#include "sorting.hpp"

#include <algorithm>
#include <iostream>
#include <random>

namespace {

bool checkInsertion(const char* name,
                    std::vector<int> values,
                    int left,
                    int right,
                    sc2001::ComparisonCount expectedComparisons) {
    auto expected = values;
    if (left <= right) {
        std::sort(expected.begin() + left, expected.begin() + right + 1);
    }

    // A nonzero start also checks that the function accumulates the count.
    sc2001::ComparisonCount comparisons = 7;
    sc2001::insertionSort(values, left, right, comparisons);
    if (values != expected || comparisons != 7 + expectedComparisons) {
        std::cerr << "FAIL: " << name << " (comparisons: "
                  << comparisons - 7 << ", expected: "
                  << expectedComparisons << ")\n";
        return false;
    }
    return true;
}

}  // namespace

int main() {
    bool passed = true;
    passed &= checkInsertion("empty", {}, 0, -1, 0);
    passed &= checkInsertion("single element", {9}, 0, 0, 0);
    passed &= checkInsertion("two sorted", {2, 5}, 0, 1, 1);
    passed &= checkInsertion("two reversed", {5, 2}, 0, 1, 1);
    passed &= checkInsertion("worked example", {5, 2, 4}, 0, 2, 3);
    passed &= checkInsertion("sorted", {1, 2, 3, 4, 5}, 0, 4, 4);
    passed &= checkInsertion("reverse sorted", {5, 4, 3, 2, 1}, 0, 4, 10);
    passed &= checkInsertion("equal values", {3, 3, 3, 3}, 0, 3, 3);
    passed &= checkInsertion("mixed duplicates", {2, 1, 2, 1}, 0, 3, 5);
    passed &= checkInsertion("inclusive subrange", {99, 5, 2, 4, -99}, 1, 3, 3);

    std::mt19937 generator(2001);
    std::uniform_int_distribution<int> distribution(-10, 10);
    for (int size = 0; size <= 50; ++size) {
        std::vector<int> values(size);
        for (int& value : values) {
            value = distribution(generator);
        }
        auto expected = values;
        std::sort(expected.begin(), expected.end());
        sc2001::ComparisonCount comparisons = 0;
        sc2001::insertionSort(values, 0, size - 1, comparisons);
        if (values != expected) {
            std::cerr << "FAIL: random array of size " << size << '\n';
            passed = false;
        }
    }

    if (!passed) {
        return 1;
    }
    std::cout << "All Insertion Sort tests passed.\n";
    return 0;
}
