# Assignment Requirements and Project Choices

Source: the one-page `Project3_26S1.pdf` in the course directory. This document summarizes the assignment and distinguishes internal implementation choices from course requirements.

## Explicit requirements

The knapsack has positive integer capacity C. There are n item types with positive integer weights and profits, and each type has an unlimited supply. Find the maximum profit P(C) achievable with total weight at most C.

| Part | Required work | Corresponding file or deliverable |
| --- | --- | --- |
| (1) | Give a recursive definition of P(C) | State, base cases, and recurrence explanation in docs/theory.md |
| (2) | Draw the subproblem graph for P(15) using the first dataset | Completed graph in docs/subproblem-graph.md |
| (3) | Give a bottom-up dynamic programming algorithm | Pseudocode and evaluation-order explanation |
| (4a) | Implement the algorithm and show P(16) for the first dataset | src/knapsack.cpp and results/case-a.txt |
| (4b) | Show P(12) for the second dataset | results/case-b.txt |

First dataset: weights=[4,5,8], profits=[7,6,9]. Second dataset: weights=[5,6,7], profits=[7,6,9]. Corresponding positions form weight-profit pairs for item types 0, 1, and 2.

## Framework choices

- Follow the earlier projects' C++17, Makefile, and include/src/tests/docs structure.
- Use a one-dimensional DP table and return the best profit for every capacity to support explanation.
- Include correctness reasoning, O(nC) time analysis, and O(C) auxiliary-space analysis.
- Use a three-person allocation, boundary tests, and full-table output for internal collaboration and validation.
- Support capacity 0 as a base-case test; the assignment itself specifies positive capacity.
- Write all Project 3 documentation and report material in English, as requested by the team. This includes headings, tables, figure labels, captions, and output explanations.

## Optional extensions

Item-count reconstruction, automatic graph export, performance experiments, and a notebook presentation may be added later. The required tasks do not depend on these extensions.

## Information not provided on the assignment sheet

Consult separate course notices for the deadline, submission platform, report or slide format, required language or programming language, team size, and any additional course rules. This framework does not invent those details; the team's English-only writing preference applies to the current materials.
