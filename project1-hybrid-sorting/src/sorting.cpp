#include "sorting.hpp"

namespace sc2001 {

void insertionSort(
    std::vector<int>& values,
    int left,
    int right,
    ComparisonCount& keyComparisons
) {
    if(left >= right){
        return;
    }

    for(int i=left+1;i<=right;++i){
        const int key=values[i];
        int j=i-1;

        while(j>=left){
            ++keyComparisons;

            if(values[j]<=key){
                break;
            }

            values[j+1]=values[j];
            --j;
        }

        values[j+1]=key;
    }
}

// Merge two adjacent sorted ranges.
void merge(
    std::vector<int>& values,
    int left,
    int middle,
    int right,
    ComparisonCount& keyComparisons
){
    std::vector<int> temporary;

    int i=left;
    int j=middle+1;

    while (i<=middle && j<=right){
        keyComparisons++;
        if (values[i]<=values[j]){
            temporary.push_back(values[i]);
            i++;
        }
        else{
            temporary.push_back(values[j]);
            j++;
        }
    }

    while(i<=middle){
        temporary.push_back(values[i]);
        ++i;
    }

    while(j<=right){
        temporary.push_back(values[j]);
        ++j;
    }

    int position=left;
    for(int value : temporary){
        values[position]=value;
        ++position;
    }
}
// Original recursive Merge Sort.
void mergeSort(
    std::vector<int>& values,
    int left,
    int right,
    ComparisonCount& keyComparisons
) {
    if (left >= right) {
        return;
    }

    int middle = left + (right - left) / 2;

    mergeSort(values, left, middle, keyComparisons);
    mergeSort(values, middle + 1, right, keyComparisons);

    merge(values, left, middle, right, keyComparisons);
}

// Hybrid Merge Sort using Insertion Sort for ranges at or below the threshold.
void hybridMergeSort(
    std::vector<int>& values,
    int left,
    int right,
    int threshold,
    ComparisonCount& keyComparisons
) {
    if(left >= right){
        return;
    }

    const int size=right-left+1;

    if(size <= threshold){
        insertionSort(values,left,right,keyComparisons);
        return;
    }

    const int middle=left+(right-left)/2;

    hybridMergeSort(
        values,
        left,
        middle,
        threshold,
        keyComparisons
    );

    hybridMergeSort(
        values,
        middle+1,
        right,
        threshold,
        keyComparisons
    );

    merge(values,left,middle,right,keyComparisons);
}

}  // namespace sc2001
