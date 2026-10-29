# Correctness Plan

`make test` checks infrastructure; `make check-solution` checks the algorithm. The core solver is currently unimplemented, so the latter reports PENDING rather than passing.

## Cases already included in algorithm acceptance

| Case | Expected result | Purpose |
| --- | --- | --- |
| Part (4a) | 28 | Select four copies of the weight-4, profit-7 item |
| Part (4b) | 16 | Select one weight-5 item and one weight-7 item |
| Part (2), capacity 15 | 21 | Select three weight-4 items; leave capacity 3 unused |
| Capacity 0 | 0 | Base case |
| Capacity 3, weights 4/5 | 0 | No item fits |
| Capacity 9, one type with weight 4 and profit 7 | 14 | Unlimited reuse and unused capacity |
| Capacity 10, weights 6/5, profits 9/7 | 14 | Profit-density greedy selection can fail |
| Capacity 6, weights 3/3, profits 4/5 | 10 | Prefer higher profit at the same weight |
| Capacity 2, weight 1, profit INT_MAX | 2 * INT_MAX | Total profit requires a 64-bit type |

For the second dataset, acceptance also checks every entry of dp[0..12]. Expected values in tests are manually derived references, not evidence that the pending program has already produced them.

## Independent validation for Member B

Write a small-capacity enumerator used only by tests. For each item type, enumerate zero, one, two, or more copies while respecting remaining capacity. At the end of the item list, compare total profits. Base the reference on combinations of item counts rather than another implementation of the DP recurrence.

Suggested scope: capacities 0..20, 1..4 item types, and small positive weights and profits. Use multiple fixed cases or a fixed random seed. On disagreement, print the full input and both answers for reproduction. This enumerator is a testing reference; the required production algorithm for part (3) remains bottom-up DP.

## Manual review

- Transitions use smaller capacities and permit repeated use of an item type.
- Every candidate respects the capacity constraint; empty selections and unused capacity are allowed.
- Optimal profit never decreases as capacity increases.
- Printed answers come from the solver's returned table, without hard-coded expected answers in main.
- If item-count reconstruction is added, its total weight and profit agree with capacity and dp[C].
