# Project schedule and milestones

This schedule starts after basic algorithm learning. Use the [execution plan](execution-plan.md) for detailed implementation and analysis instructions. The deadline and member names remain unconfirmed; D1 is a relative working day.

## Suggested eight-day schedule

| Day | Tasks | Acceptance criterion |
| --- | --- | --- |
| D1 | A/B read the provided framework and start matrix/heap implementation | Shared fixtures used; own-module tests guide progress |
| D2 | A/B continue algorithms; C starts generator/output integration on the next evening | Matrix/heap progress plus exact input generation |
| D3 | Heap Dijkstra, edge cases, independent random reference checks | Both algorithms pass the correctness gate |
| D4 | C++ timing/count CLI, Python runner and metadata | One graph completes the entire measurement pipeline |
| D5 | Pilot, summary script, theoretical write-up | Timing rules and actual parameter table are fixed |
| D6 | Main experiments on one machine/build | Raw data and environment records are complete |
| D7 | Aggregate, plot, analyze parts (a) and (b) | Four main charts trace to source CSV |
| D8 | Compare for (c), finish report, reproduce a subset | All members explain conclusions and deliverables |

Allow another one or two days for debugging and submission checks if possible. If time is short, reduce optional experiments and polish before reducing correctness checks.

## Dependencies

Contracts → graph representations → matrix algorithm and independent heap → heap algorithm → correctness gate → measurement pipeline → pilot → main experiments → analysis → report.

Graph generation and reference tests can progress while algorithm modules are being written. Main measurement waits for both implementations to pass.

## Milestone checklist

- [ ] M1: shared representations and build entry points.
- [ ] M2: both algorithms and the indexed heap.
- [ ] M3: hand cases, boundaries, heap invariants, independent random validation.
- [ ] M4: pilot, trustworthy timing boundaries, raw CSV, environment records.
- [ ] M5: three main experiment suites.
- [ ] M6: per-graph summaries, paired ratios, four charts and explanations.
- [ ] M7: theory, empirical analysis, conditional comparison, reproducibility and course submission checks.

## Risks

Heap failures: isolate heap tests before debugging the graph algorithm. Resource pressure: estimate matrix storage and pilot the largest inputs. Short timings: preserve high-resolution values and increase scale/repetitions if needed. Unexpected trends: check input equivalence, build, counters, and measurement boundaries before interpreting.

The shared graph conversion and build scaffold are available. Algorithm correctness, generation and C++ measurement entry points are complete. Python automation, formal measurements, plots and the English result report are now complete. Team review and adaptation to any separately announced submission format remain to be done. See [framework guide](framework-guide.md) and [updated roles](team-roles.md).
