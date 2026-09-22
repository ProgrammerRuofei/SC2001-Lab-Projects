# Part C(ii) Retest Report Package

This directory contains the report, raw data, derived statistics, figures, and
reproduction scripts for the second dense Part C(ii) retest conducted on
2026-09-22.

The retest examines the apparent `S = 62` anomaly. The comparison-count change
at the `61/62` boundary is an expected consequence of the recursion-tree
structure. However, the isolated CPU-time peak previously observed at `S = 62`
was not reproduced and is best interpreted as timing noise rather than an
algorithm-specific anomaly.

## Contents

- Full report: `part-c-ii-analysis-en.md`
- Raw data and derived statistics: `data/`
- Report figures: `figures/`
- Analysis and figure-generation scripts: `scripts/`

## Directory Structure

```text
part-c-ii-retest-20260922/
|-- README.md
|-- part-c-ii-analysis-en.md
|-- data/
|   |-- fixed_n_1m_boundary_dense_repeated_20260922_retest.csv
|   |-- fixed_n_1m_boundary_dense_repeated_20260922_retest.meta.json
|   |-- fixed_n_1m_boundary_dense_repeated_20260922_retest_summary.csv
|   |-- fixed_n_1m_boundary_dense_repeated_20260922_retest_regions.csv
|   `-- fixed_n_1m_boundary_dense_repeated_20260922_retest_paired.csv
|-- figures/
|   |-- comparisons_vs_s.svg
|   |-- cpu_time_vs_s.svg
|   |-- boundary_61_65.svg
|   |-- boundary_121_123.svg
|   `-- timing_session_drift.svg
`-- scripts/
    |-- prepare_retest_report.py
    `-- compare_session_drift.py
```

## Dataset Scope

- Input size: `n = 1,000,000`
- Thresholds: 76 values covering `S = 32–260`, with dense sampling around
  three recursion boundaries
- Random seeds: 15
- Timed sorts per recorded case: 5
- Raw records: 1,140

The report and figures were generated from the latest retest data in this
directory's `data/` folder. All figure links in the report use relative paths
within this package.

## Reproducing the Summaries and Figures

Run the following command from this directory in PowerShell:

```powershell
python scripts/prepare_retest_report.py `
  --input data/fixed_n_1m_boundary_dense_repeated_20260922_retest.csv `
  --summary data/fixed_n_1m_boundary_dense_repeated_20260922_retest_summary.csv `
  --regions data/fixed_n_1m_boundary_dense_repeated_20260922_retest_regions.csv `
  --paired data/fixed_n_1m_boundary_dense_repeated_20260922_retest_paired.csv `
  --figure-dir figures
```

The script uses only the Python standard library; no additional plotting
package is required.
