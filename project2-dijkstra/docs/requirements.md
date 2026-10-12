# Requirements and proposed decisions

## Explicit course requirements

The supplied Project 2 specification requires:

| Part | Implementation | Analysis |
| --- | --- | --- |
| (a) | Adjacency matrix and array priority queue | Theoretical and empirical time complexity in terms of vertex and edge counts |
| (b) | Array of adjacency lists and minimizing heap | Theoretical and empirical time complexity in terms of vertex and edge counts |
| (c) | Compare the two implementations | Discuss which is better and under what circumstances |

Let n=|V| and m=|E|. Explain how m changes with n in each experiment, and include a fixed-n experiment that varies m.

## Proposed decisions

C++17 implements both algorithms; Python runs batches and plots results. Main experiments use simple connected undirected graphs, source 0, and integer weights in [1,1000]. Tests also cover zero-weight edges and disconnected graphs. Negative weights are rejected.

Part (a) performs linear minimum selection in unsorted arrays. Part (b) uses an indexed binary min-heap: one entry per vertex, with decrease-key. Results contain distances and predecessors.

An undirected logical edge counts once toward m and twice in adjacency-list storage. Thus the total number of list entries is 2m.

## Still to confirm

The PDF does not specify the deadline, submission channel, language, group size, report length, presentation requirements, permitted heap libraries, or AI-assistance policy. Check additional course instructions before submission.

## Completion checklist

- [ ] Both implementations use the required structures and pass independent correctness checks.
- [ ] Complexity derivations match the actual heap implementation.
- [ ] Sparse growth, dense growth, and fixed-n varying-m experiments are complete.
- [ ] Raw measurements, seeds, environment, and aggregation rules are preserved.
- [ ] Figures support conditional comparisons rather than universal performance claims.
- [ ] Every member can trace both implementations and explain the results.

Current status: infrastructure and explicit implementation scaffolds. Core implementations and correctness checks are complete. Pilot output is available; formal main experiments and empirical conclusions remain pending.
