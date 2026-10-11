# Planned figures

No figures have been generated.

1. sparse-time-vs-n.png: m=4n, time against n for both algorithms.
2. dense-time-vs-n.png: target density 0.5, time against n.
3. density-time.png: n=1000, time against actual density or m.
4. density-speedup.png: n=1000, paired matrix/heap ratio with reference line 1.
5. Optional diagnostic charts: matrix scans against n², list scans against 2m, decrease-key counts against m.

Store each run's charts under figures/<run_id>/. Label units, graph type, sample counts, aggregation, and the meaning of error bars. Every chart must trace to CSV and run ID, with an explanation of the conclusion it supports.
