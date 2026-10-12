# Completed experiment results

Run main-v1 covers 19 configurations, 95 graphs, 1330 paired timing rows and 190 separate counter records. Complete validated tables are in results/main-v1; charts are in figures/main-v1.

Read [the experimental report](report-draft.md) for the theoretical/empirical explanations and the guide coverage checklist. The main observation is that lists/indexed heap wins on every tested graph median; its advantage decreases with density, but no crossover is observed up to 90% density. This is conditional on the tested graph family and machine.

- [Summary CSV](../results/main-v1/summary.csv)
- [Paired ratio summary](../results/main-v1/paired_speedup_summary.csv)
- [Validation manifest](../results/main-v1/validation.json)
- [Environment and commands](../results/main-v1/environment.json)
- [Four-panel overview](../figures/main-v1/overview.png)
- [Operation diagnostics](../figures/main-v1/operation-counts.png)

Raw measurements are local in results/raw/main-v1 and ignored by Git. The report states what is and is not empirically demonstrated; it does not assume a crossover or claim that finite data prove Big-O.
