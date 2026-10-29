# Theory and Algorithm Design Prompts

This is a worksheet for parts (1) and (3). The state definition and reasoning direction are provided. Team members should complete the proof, pseudocode, and manual trace before including them in the final report.

## State and recurrence

P(c) is the maximum profit achievable with total weight at most c. Every item type may be selected repeatedly, and unused capacity is allowed.

```text
P(0) = 0
P(c) = max({0} union {p[i] + P(c - w[i]) | 0 <= i < n, w[i] <= c})
```

Including 0 in the candidate set makes the answer 0 when no item fits. Only nonnegative capacities are accessed, so P need not be defined for negative capacities. Every weight is positive, making each dependency strictly smaller than the current capacity.

Consider removing one item of type i from a nonempty optimal selection. Why must the remaining selection achieve the optimum for capacity c-w[i]? What would happen if it could be replaced by a better selection? Also explain why every recurrence candidate is feasible at capacity c.

**TODO A:** Turn this reasoning into a complete correctness explanation covering both empty and nonempty selections.

## Bottom-up design

Fill the table in increasing capacity order and consider every item that fits. Smaller states may already contain the same item type, so the state definition permits unlimited reuse.

**TODO A:** Write pseudocode for initialization, the outer capacity loop, the inner item loop, the feasibility condition, the update, and the return value. Keep it consistent with src/knapsack.cpp.

**TODO all members:** Manually fill capacities 0 through 12 for the second dataset. Explain the changes at capacities 5, 7, 10, and 12. Keep the at-most-capacity interpretation consistent throughout; exact-fill unreachable-state semantics do not apply here.

## Complexity

There are C+1 capacity states, and each nonzero capacity examines at most n item types. Time complexity is O(nC), and DP auxiliary space is O(C). The input items occupy O(n) space. Relative to the binary encoding length of the input, O(nC) is pseudo-polynomial because the numeric value of C can greatly exceed the number of bits needed to represent it.

**TODO A/C:** Justify these bounds using the loops and arrays in the final implementation. The assignment does not explicitly require performance experiments; the complexity explanation can be completed directly from the algorithm.
