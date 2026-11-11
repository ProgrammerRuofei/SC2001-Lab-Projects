# Theory and Algorithm Design

Let P(c) be the best profit with total weight at most c. With positive weights and unlimited copies,

```text
P(0) = 0
P(c) = max({0} ∪ {p[i] + P(c - w[i]) : 0 ≤ i < n, w[i] ≤ c}).
```

The zero candidate is the empty selection. Each other candidate is feasible because the item and the selection for c − w[i] fit together. For any nonempty optimal selection, remove one item i. If the remainder were not optimal for c − w[i], replacing it with a better feasible selection would contradict optimality. Thus the recurrence includes an optimal candidate. Positive weights make every dependency smaller.

```text
dp[0..C] ← 0
for c ← 1 to C:
    for each item i:
        if w[i] ≤ c:
            dp[c] ← max(dp[c], p[i] + dp[c − w[i]])
return dp
```

Ascending capacities ensure all dependencies are ready; the previous state may already contain item i, permitting reuse. Induction over c proves the table follows the recurrence. The O(nC) time bound follows from the nested loops, and the O(C) auxiliary space bound from the table; the input occupies O(n) space. The time is pseudo-polynomial in the binary input length.

For weights [5, 6, 7] and profits [7, 6, 9], capacities 0 through 12 have values [0, 0, 0, 0, 0, 7, 7, 9, 9, 9, 14, 14, 16]. The value rises at 5 (one weight-5 item), 7 (one weight-7 item), 10 (two weight-5 items), and 12 (weight 5 plus weight 7). Unused capacity is allowed throughout.
