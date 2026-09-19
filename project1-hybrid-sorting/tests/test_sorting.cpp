#include "sorting.hpp"

#include <iostream>

int main() {
    // Small correctness tests must pass before performance experiments.
    std::vector<int> values={2,6,9,1,3,7,8};
    const std::vector<int> expected={1,2,3,6,7,8,9};
    sc2001::ComparisonCount keyComparisons=0;

    sc2001::merge(values,0,2,6,keyComparisons);

    if(values != expected){
        std::cerr<<"FAIL: merge produced the wrong order\n";
        return 1;
    }

    if (keyComparisons!=6){
        std::cerr<<"FAIL: expected 6 key comparisons, got "
                 <<keyComparisons<<'\n';
        return 1;
    }

    std::cout << "PASS: basic merge test\n";

    std::vector<int> mergeSortValues={8,3,5,1};
    const std::vector<int> mergeSortExpected={1,3,5,8};
    sc2001::ComparisonCount mergeSortComparisons=0;

    sc2001::mergeSort(
        mergeSortValues,
        0,
        static_cast<int>(mergeSortValues.size())-1,
        mergeSortComparisons
    );

    if(mergeSortValues != mergeSortExpected){
        std::cerr<<"FAIL: merge sort produced the wrong order\n";
        return 1;
    }

    if(mergeSortComparisons != 5){
        std::cerr<<"FAIL: expected 5 merge sort key comparisons, got "
                 <<mergeSortComparisons<<'\n';
        return 1;
    }

    std::cout<<"PASS: basic merge sort test\n";

    std::vector<int> singleValue={42};
    const std::vector<int> singleExpected={42};
    sc2001::ComparisonCount singleComparisons=0;

    sc2001::mergeSort(singleValue,0,0,singleComparisons);

    if(singleValue != singleExpected){
        std::cerr<<"FAIL: single-element merge sort test\n";
        return 1;
    }

    if(singleComparisons != 0){
        std::cerr<<"FAIL: a single element should require 0 key comparisons\n";
        return 1;
    }

    std::cout<<"PASS: single-element merge sort test\n";

    std::vector<int> sortedValues={1,2,3,4};
    const std::vector<int> sortedExpected={1,2,3,4};
    sc2001::ComparisonCount sortedComparisons=0;

    sc2001::mergeSort(sortedValues,0,3,sortedComparisons);

    if(sortedValues != sortedExpected){
        std::cerr<<"FAIL: already-sorted merge sort test\n";
        return 1;
    }

    std::cout<<"PASS: already-sorted merge sort test\n";

    std::vector<int> reverseValues={4,3,2,1};
    const std::vector<int> reverseExpected={1,2,3,4};
    sc2001::ComparisonCount reverseComparisons=0;

    sc2001::mergeSort(reverseValues,0,3,reverseComparisons);

    if(reverseValues != reverseExpected){
        std::cerr<<"FAIL: reverse-sorted merge sort test\n";
        return 1;
    }

    std::cout<<"PASS: reverse-sorted merge sort test\n";

    std::vector<int> duplicateValues={3,1,3,1};
    const std::vector<int> duplicateExpected={1,1,3,3};
    sc2001::ComparisonCount duplicateComparisons=0;

    sc2001::mergeSort(duplicateValues,0,3,duplicateComparisons);

    if(duplicateValues != duplicateExpected){
        std::cerr<<"FAIL: duplicate-value merge sort test\n";
        return 1;
    }

    std::cout<<"PASS: duplicate-value merge sort test\n";

    std::vector<int> subarrayValues={99,8,3,5,1,77};
    const std::vector<int> subarrayExpected={99,1,3,5,8,77};
    sc2001::ComparisonCount subarrayComparisons=0;

    sc2001::mergeSort(subarrayValues,1,4,subarrayComparisons);

    if(subarrayValues != subarrayExpected){
        std::cerr<<"FAIL: non-zero-start subarray merge sort test\n";
        return 1;
    }

    std::cout<<"PASS: non-zero-start subarray merge sort test\n";
    return 0;
}
