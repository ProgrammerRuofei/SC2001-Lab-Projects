# Three-person work allocation suggestion

This is a proposed internal allocation, not an additional course requirement.
It assumes that the member requesting a stronger algorithm role is Member A.
Replace A, B, and C with names after the team agrees.

## Shared-participation rule

The work is not divided into three isolated areas. Every member should:

- personally implement and explain at least one core sorting component;
- add or review correctness tests;
- run at least one part of the measured experiments;
- inspect the source CSV data and review at least one figure;
- contribute to the theoretical comparison and final presentation;
- review code written by another member.

The allocation below changes the amount of work in each area, but no member is
excluded from algorithms, experiments, or visualization.

## Member A - Algorithm-weighted allocation

A takes a larger share of algorithm design while still participating in the
experimental work.

Personal implementation:

- implement the two-pointer Merge operation;
- implement original recursive Merge Sort;
- place and justify the relevant key-comparison increments;
- explain the recursion tree, base case, inclusive boundaries, and
  `Theta(n log n)` behavior.

Tests and review:

- add focused tests for merging, duplicates, uneven halves, and recursion
  boundaries;
- review C's Hybrid Merge Sort, especially the threshold location and recursion;
- review B's Insertion Sort comparison-counting logic.

Experiments and presentation:

- implement the C++ comparison/timing output with B and C reviewing the format;
- run and interpret the original-versus-hybrid experiment on 10,000,000
  integers;
- connect measured trends to the algorithmic analysis;
- review every final chart for whether it supports the stated conclusion.

## Member B - Insertion Sort, testing, and input allocation

B has a complete core algorithm contribution and a substantial role in testing
and the comparisons-versus-`n` study.

Personal implementation:

- implement Insertion Sort for the inclusive range `[left, right]`;
- place and justify comparisons between the saved key and array values;
- explain the sorted-prefix invariant and `O(n^2)` behavior.

Tests and review:

- build much of the shared small correctness-test suite;
- cover one element, two elements, sorted, reverse-sorted, duplicates, random
  small arrays, `S = 1`, and `S >= array size`;
- manually trace and review A's Merge implementation;
- verify that comparison counts follow
  [`comparison-counting.md`](comparison-counting.md).

Experiments and visualization:

- implement or coordinate reproducible random-array generation in C++;
- run the fixed-`S`, varying-`n` experiment;
- prepare the first comparisons-versus-`n` chart together with C;
- write the empirical-versus-theoretical explanation for that chart;
- independently check at least one other final figure against its CSV data.

## Member C - Hybrid, automation, and visualization allocation

C has a complete core algorithm contribution and a larger share of experiment
automation and visualization.

Personal implementation:

- implement Hybrid Merge Sort after Insertion Sort, Merge, and original Merge
  Sort have passed review;
- decide and justify where `size <= S` belongs;
- ensure that the threshold check is not counted as a key comparison;
- explain why fixed-`S` hybridization changes practical constants but not the
  overall large-`n` asymptotic behavior.

Tests and review:

- add hybrid-specific tests, especially `S = 1`, `S >= array size`, and
  transitions around the threshold;
- review A's original Merge Sort recursion and base case;
- review B's random-data generation and reproducibility settings.

Experiments and visualization:

- implement Python automation for repeated runs and CSV processing;
- run the fixed-`n`, varying-`S` experiment with A or B checking the output;
- prepare the comparisons-versus-`S` and suitable-`S` figures;
- coordinate consistent labels, units, sample counts, and styles across figures;
- explain why minimum key comparisons and minimum CPU time may occur at
  different values of `S`.

## Core-code participation matrix

| Component | First implementation | Required review and participation |
| --- | --- | --- |
| Insertion Sort | B | A checks counting; C checks hybrid compatibility |
| Merge | A | B manually traces it; C checks temporary-range boundaries |
| Original Merge Sort | A | B checks the base case; C checks recursion behavior |
| Hybrid Merge Sort | C | A reviews algorithm structure; B tests threshold cases |

Each member must be able to trace all four components even when they did not
write the first implementation.

## Experiment and visualization participation matrix

| Work item | Main hands-on contribution | Contributions from the other members |
| --- | --- | --- |
| Random datasets | B writes generator | A checks cost; C records seed/parameters |
| C++ measurement output | A writes first version | B validates counts; C validates CSV format |
| Python automation | C writes first version | A and B run and review it |
| Fixed `S`, varying `n` | B runs and drafts chart | A explains theory; C checks visualization |
| Fixed `n`, varying `S` | C runs and drafts chart | B checks data; A explains trade-off |
| Suitable `S` across sizes | C aggregates results | A interprets algorithms; B checks repeatability |
| Original versus hybrid at 10M | A runs comparison | B checks inputs/timing; C prepares table/figure |
| Final analysis and slides | All three | Each presents and reviews another member's part |

“Main hands-on contribution” is not sole ownership. At least one other member
must reproduce or verify each experimental conclusion.

## Suggested branch sequence

To reduce conflicts in the shared `sorting.cpp` file:

1. B works on `feature/insertion-sort`.
2. A works on `feature/merge-sort`, coordinating the separate code region with
   B.
3. Both branches are reviewed and merged into `develop`.
4. C updates from `develop` and works on `feature/hybrid-sort`.
5. Experiment infrastructure begins only after the correctness gate passes.

While A and B are implementing core code, C can prepare test cases, CSV format
proposals, and experiment documentation without implementing their algorithms.
A and B then review and use that infrastructure so it is not understood by only
one person.

## Correctness gate before experiments

All three members jointly confirm:

- the program matches a trusted sorted result for every small test;
- inclusive range assumptions are consistent;
- no out-of-bounds or off-by-one errors remain;
- key comparisons follow the documented convention;
- `S = 1` and `S >= array size` behave correctly;
- all current tests pass from a clean build.

Large experiments should not begin until everyone agrees that this gate passes.

## AI-assisted development boundary

AI assistance may be used for:

- explaining syntax, invariants, recursion, and edge cases;
- reviewing member-written code and giving repair hints;
- suggesting tests without hiding the algorithm inside the test;
- diagnosing compilation or runtime errors after a member attempts a solution;
- scaffolding build tools and experiment infrastructure;
- helping with CSV processing, plotting, documentation, and presentation text.

The team members should personally:

- write the bodies of Insertion Sort, Merge, original Merge Sort, and Hybrid
  Merge Sort;
- choose and explain the algorithm control flow and indexing;
- place and justify every key-comparison increment;
- manually trace small inputs;
- understand, test, and take responsibility for any AI-assisted non-core code.

No AI-generated code should be merged simply because it compiles. Its human
reviewer must be able to explain its data flow, assumptions, and output.

## Final integration

Before merging `develop` into `main`:

1. Each member reviews another member's code and one experimental result.
2. All tests and the clean build pass.
3. Every figure is checked against its CSV source.
4. All three members can explain the algorithm and measurement convention.
5. All three members confirm the final pull request.

