#include "sorting.hpp"

namespace sc2001 {

// TODO(student): Implement Insertion Sort here.

// TODO(student): Implement the two-pointer merge operation here.
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
// TODO(student): Implement original Merge Sort here.
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

// TODO(student): Implement Hybrid Merge Sort here after the earlier algorithms
// have been implemented and tested.

}  // namespace sc2001
