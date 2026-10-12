"""Test-only fixtures verify aggregation math and rejection of corrupt datasets."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"experiments/scripts"))
from experiment_common import jobs_from_config, quantile, read_csv, write_csv
from summarize_results import summarize


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="sc2001-analysis-test-")
        self.root=Path(self.temp.name)
        self.run=self.root/"raw";self.run.mkdir()
        config=self.run/"config.csv"
        write_csv(config,[dict(suite="test_fixture",n=3,m=2,requested_density="",weight_min=1,
            weight_max=20,source=0,graph_seeds="1;2;3",warmup_repeats=0,timing_repeats=2)])
        jobs=jobs_from_config(config)
        timing=[];counts=[]
        matrix_times=[[2,4],[10,14],[100,100]]
        heap_times=[[10,10],[1,1],[4,4]]
        for i,job in enumerate(jobs):
            job["graph_id"]=f"fixture-{i}"
            for sample in range(2):
                for position,(algorithm,values) in enumerate([
                        ("matrix_array",matrix_times[i]),("list_indexed_heap",heap_times[i])]):
                    timing.append(dict(run_id="unit-test",suite=job["suite"],graph_id=job["graph_id"],
                        n=3,m=2,actual_density=2/3,graph_seed=job["graph_seed"],source=0,
                        weight_min=1,weight_max=20,algorithm=algorithm,sample_index=sample,
                        order_seed=job["order_seed"],order_in_pair=position,elapsed_ms=values[sample],
                        distances_match="true",status="ok"))
            for algorithm in ["matrix_array","list_indexed_heap"]:
                matrix=algorithm=="matrix_array"
                counts.append(dict(run_id="unit-test",suite=job["suite"],graph_id=job["graph_id"],
                    n=3,m=2,graph_seed=job["graph_seed"],algorithm=algorithm,
                    min_scan_slots=9 if matrix else 0,matrix_scan_slots=9 if matrix else 0,
                    adjacency_entries_scanned=0 if matrix else 4,relax_attempts=2,relax_successes=2,
                    heap_inserts=0 if matrix else 3,heap_extracts=0 if matrix else 3,heap_decreases=0))
        self.timing=timing;self.counts=counts
        self.env=dict(run_id="unit-test",status="complete",jobs=jobs,timing_rows=12,count_rows=6)
        self.save()

    def tearDown(self):self.temp.cleanup()
    def save(self):
        write_csv(self.run/"timings.csv",self.timing)
        write_csv(self.run/"counts.csv",self.counts)
        (self.run/"environment.json").write_text(json.dumps(self.env))
    def analyze(self):return summarize(self.run,self.root/"summary")
    def test_math(self):
        self.analyze()
        rows=read_csv(self.root/"summary/summary.csv")
        a=next(r for r in rows if r["algorithm"]=="matrix_array")
        self.assertEqual(float(a["median_ms"]),12)
        self.assertEqual(float(a["q1_ms"]),7.5)
        ratio=read_csv(self.root/"summary/paired_speedup_summary.csv")[0]
        self.assertEqual(float(ratio["median_ratio"]),12)  # not ratio of aggregate medians
        self.assertEqual(quantile([1],.75),1)
    def test_missing_sample(self):
        self.timing.pop();self.env["timing_rows"]-=1;self.save()
        with self.assertRaises(ValueError):self.analyze()
    def test_duplicate_pair(self):
        self.timing[1]=copy.deepcopy(self.timing[0]);self.save()
        with self.assertRaises(ValueError):self.analyze()
    def test_nonfinite_time(self):
        self.timing[0]["elapsed_ms"]="nan";self.save()
        with self.assertRaises(ValueError):self.analyze()
    def test_bad_counts(self):
        self.counts[0]["matrix_scan_slots"]=8;self.save()
        with self.assertRaises(ValueError):self.analyze()
    def test_failed_run(self):
        self.env["status"]="failed";self.save()
        with self.assertRaises(ValueError):self.analyze()
    def test_unpaired_graph(self):
        self.counts[0]["graph_id"]="unknown";self.save()
        with self.assertRaises(ValueError):self.analyze()
    def test_duplicate_configuration(self):
        rows=read_csv(self.run/"config.csv");write_csv(self.run/"bad.csv",rows+rows)
        with self.assertRaises(ValueError):jobs_from_config(self.run/"bad.csv")


if __name__=="__main__":unittest.main()
