# Presentation notes

This file is a running record of theoretical points for the final presentation. It does not contain experimental results.

- Insertion Sort takes `O(n^2)` time in the general/worst-case discussion and has low overhead on small subarrays.
- Merge Sort takes `Theta(n log n)` time because it has logarithmically many recursion levels and linear merging work per level.
- For fixed `S`, hybridization reduces practical overhead and changes constant factors without changing the overall large-`n` asymptotic behavior.
- `S` controls a trade-off: more recursive Merge Sort work at smaller `S`, versus more quadratic Insertion Sort work inside larger subarrays at larger `S`.
- The `S` producing the fewest key comparisons may differ from the `S` producing the lowest CPU time because timing also reflects recursion, copying, memory access, branches, and other non-key-comparison costs.

