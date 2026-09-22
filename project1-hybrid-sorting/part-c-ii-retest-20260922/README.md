# Part (c)(ii) 最新复测报告包

本文件夹集中保存 2026-09-22 第二轮密集复测的报告、原始数据、派生统计表、图表和复现脚本。

## 入口

- 完整中文报告：`part-c-ii-analysis-zh.md`
- Complete English report: `part-c-ii-analysis-en.md`
- 原始数据与统计结果：`data/`
- 报告图表：`figures/`
- 分析与制图脚本：`scripts/`

## 文件结构

```text
part-c-ii-retest-20260922/
├── README.md
├── part-c-ii-analysis-en.md
├── part-c-ii-analysis-zh.md
├── data/
│   ├── fixed_n_1m_boundary_dense_repeated_20260922_retest.csv
│   ├── fixed_n_1m_boundary_dense_repeated_20260922_retest.meta.json
│   ├── fixed_n_1m_boundary_dense_repeated_20260922_retest_summary.csv
│   ├── fixed_n_1m_boundary_dense_repeated_20260922_retest_regions.csv
│   └── fixed_n_1m_boundary_dense_repeated_20260922_retest_paired.csv
├── figures/
│   ├── comparisons_vs_s.svg
│   ├── cpu_time_vs_s.svg
│   ├── boundary_61_65.svg
│   ├── boundary_121_123.svg
│   └── timing_session_drift.svg
└── scripts/
    ├── prepare_retest_report.py
    └── compare_session_drift.py
```

## 数据范围

- `n = 1,000,000`
- 76 个阈值，覆盖 `S = 32–260` 并加密三个递归边界
- 15 个随机 seed
- 每条记录内部 5 次排序
- 1,140 条原始记录

报告和图表均使用本文件夹 `data/` 中的最新复测数据生成，图片链接均为文件夹内部相对路径。

## 重新生成汇总表和图表

在本文件夹中运行：

```text
python scripts/prepare_retest_report.py \
  --input data/fixed_n_1m_boundary_dense_repeated_20260922_retest.csv \
  --summary data/fixed_n_1m_boundary_dense_repeated_20260922_retest_summary.csv \
  --regions data/fixed_n_1m_boundary_dense_repeated_20260922_retest_regions.csv \
  --paired data/fixed_n_1m_boundary_dense_repeated_20260922_retest_paired.csv \
  --figure-dir figures
```

该脚本只使用 Python 标准库，不需要额外安装绘图库。
