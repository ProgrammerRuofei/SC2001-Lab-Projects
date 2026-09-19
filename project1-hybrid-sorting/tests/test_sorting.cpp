#include "sorting.hpp"

#include <algorithm>
#include <iostream>
#include <random>

namespace {

bool checkInsertion(
    const char* name,
    std::vector<int> values,
    int left,
    int right,
    sc2001::ComparisonCount expectedComparisons
) {
    std::vector<int> expected=values;

    if(left<=right){
        std::sort(expected.begin()+left,expected.begin()+right+1);
    }

    sc2001::ComparisonCount comparisons=7;
    sc2001::insertionSort(values,left,right,comparisons);

    if(values != expected || comparisons != 7+expectedComparisons){
        std::cerr<<"FAIL: "<<name<<" (comparisons: "
                 <<comparisons-7<<", expected: "
                 <<expectedComparisons<<")\n";
        return false;
    }

    return true;
}

}  // namespace

int main() {
    // Small correctness tests must pass before performance experiments.
    bool insertionTestsPassed=true;
    insertionTestsPassed &= checkInsertion("empty",{},0,-1,0);
    insertionTestsPassed &= checkInsertion("single element",{9},0,0,0);
    insertionTestsPassed &= checkInsertion("two sorted",{2,5},0,1,1);
    insertionTestsPassed &= checkInsertion("two reversed",{5,2},0,1,1);
    insertionTestsPassed &= checkInsertion("worked example",{5,2,4},0,2,3);
    insertionTestsPassed &= checkInsertion("sorted",{1,2,3,4,5},0,4,4);
    insertionTestsPassed &= checkInsertion("reverse sorted",{5,4,3,2,1},0,4,10);
    insertionTestsPassed &= checkInsertion("equal values",{3,3,3,3},0,3,3);
    insertionTestsPassed &= checkInsertion("mixed duplicates",{2,1,2,1},0,3,5);
    insertionTestsPassed &= checkInsertion(
        "inclusive subrange",
        {99,5,2,4,-99},
        1,
        3,
        3
    );

    std::mt19937 generator(2001);
    std::uniform_int_distribution<int> distribution(-10,10);

    for(int size=0;size<=50;++size){
        std::vector<int> randomValues(size);

        for(int& value : randomValues){
            value=distribution(generator);
        }

        std::vector<int> randomExpected=randomValues;
        std::sort(randomExpected.begin(),randomExpected.end());

        sc2001::ComparisonCount randomComparisons=0;
        sc2001::insertionSort(
            randomValues,
            0,
            size-1,
            randomComparisons
        );

        if(randomValues != randomExpected){
            std::cerr<<"FAIL: random insertion sort array of size "
                     <<size<<'\n';
            insertionTestsPassed=false;
        }
    }

    if(!insertionTestsPassed){
        return 1;
    }

    std::cout<<"PASS: all insertion sort tests\n";

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
