# Experiment inputs and planned workflow

Configuration tables and CLI scaffold scripts exist; runner and analysis processing remain pending.

- [pilot.csv](configs/pilot.csv): small checks plus largest proposed matrix/dense inputs.
- [main.csv](configs/main.csv): sparse growth, dense growth, and fixed-n varying-density suites.
- [optional-fixed-m.csv](configs/optional-fixed-m.csv): secondary fixed-m study.

Seeds are semicolon-separated. timing_repeats and warmup_repeats are per graph per algorithm. requested_density is a target; actual density is m/(n(n-1)/2) after rounding. Sparse rows use exact m=4n and leave requested_density empty.

Pass the [correctness gate](../docs/correctness-plan.md) before measurement. Read the [experiment plan](../docs/experiment-plan.md) for parameters and the [execution plan](../docs/execution-plan.md) for planned commands. The scripts provide --help and explicitly report PENDING for actual processing. Formal runs require their TODO implementations.
