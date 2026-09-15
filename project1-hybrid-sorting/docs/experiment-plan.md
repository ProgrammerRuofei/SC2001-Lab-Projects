# Experiment plan

This plan follows the Project 1 specification. It contains no experimental results.

## 1. Generate input data

Generate random integer arrays with increasing input sizes from 1,000 through 10,000,000. Values must be in `[1, x]`, where the team will choose and document `x`.

## 2. Key comparisons versus input size

Hold `S` fixed, run the hybrid algorithm for different values of `n`, record key comparisons, and compare the empirical trend with the theoretical analysis.

Proposed values only (not course requirements):

- `n`: 1,000; 10,000; 100,000; 1,000,000; 10,000,000
- fixed `S`: to be selected after correctness testing and initial trials

## 3. Key comparisons versus threshold

Hold `n` fixed, vary `S`, record key comparisons, and compare the empirical trend with the theoretical analysis.

Proposed values only (not course requirements):

- fixed `n`: 1,000,000
- `S`: 1, 5, 10, 20, 30, 40, 50, 100

## 4. Select a suitable threshold

Use multiple input sizes to study how a suitable or optimal `S` changes. State the performance measure used when describing an optimum.

## 5. Compare with original Merge Sort

For an input containing 10,000,000 integers, compare original Merge Sort with the hybrid algorithm using:

- number of key comparisons;
- CPU time;
- the selected value of `S` for the hybrid algorithm.

