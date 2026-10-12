"""Create report-ready plots from validated summaries, never synthetic timings."""
import argparse
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR", tempfile.mkdtemp(prefix="sc2001-mpl-"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from experiment_common import digest, read_csv

COLORS = {"matrix_array":"#D97706", "list_indexed_heap":"#087F8C"}
LABELS = {"matrix_array":"Matrix + array", "list_indexed_heap":"Lists + indexed heap"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir",required=True,type=Path)
    parser.add_argument("--output-dir",required=True,type=Path)
    parser.add_argument("--overwrite",action="store_true",help="Regenerate named figure files in an existing directory")
    args=parser.parse_args()
    source,target=args.input_dir.resolve(),args.output_dir.resolve()
    validation=json.loads((source/"validation.json").read_text())
    if validation["status"]!="complete":raise ValueError("Incomplete summary")
    rows=read_csv(source/"summary.csv")
    ratios=read_csv(source/"paired_speedup_summary.csv")
    target.mkdir(parents=True,exist_ok=args.overwrite)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.titlesize":13,
                         "axes.spines.top":False,"axes.spines.right":False,"figure.facecolor":"white",
                         "axes.labelcolor":"#263238","text.color":"#263238","svg.fonttype":"none"})
    first=rows[0]
    note=f"Median of graph medians; bars: Q1–Q3 across {first['graph_count']} graph{'s' if int(first['graph_count']) != 1 else ''}; {first['timing_repeats']} timed calls per graph."
    manifest={"run_id":first["run_id"],"matplotlib":matplotlib.__version__,
        "plot_script_sha256":digest(Path(__file__)),"summary_sha256":digest(source/"summary.csv"),"ratio_summary_sha256":digest(source/"paired_speedup_summary.csv"),
        "error_bars":"Q1-Q3 across graph-level medians, not confidence intervals","figures":[]}

    def save(fig,name,caption):
        fig.savefig(target/(name+".png"),dpi=180)
        fig.savefig(target/(name+".svg"))
        plt.close(fig)
        manifest["figures"].append({"name":name,"caption":caption,"files":[name+".png",name+".svg"]})

    def finish(fig):
        fig.text(.5,.025,note,ha="center",fontsize=9,color="#546E7A")
        fig.tight_layout(rect=(0,.075,1,.97))

    def times(ax,suite,title,density=False):
        for algorithm in COLORS:
            selected=sorted([r for r in rows if r["suite"]==suite and r["algorithm"]==algorithm],
                            key=lambda r:float(r["actual_density"] if density else r["n"]))
            if not selected:raise ValueError("Missing plot suite "+suite)
            x=[100*float(r["actual_density"]) if density else int(r["n"]) for r in selected]
            y=[float(r["median_ms"]) for r in selected]
            error=[[float(r["median_ms"])-float(r["q1_ms"]) for r in selected],
                   [float(r["q3_ms"])-float(r["median_ms"]) for r in selected]]
            ax.errorbar(x,y,yerr=error,label=LABELS[algorithm],color=COLORS[algorithm],
                        marker="o",markersize=5,capsize=3,linewidth=1.8)
        ax.set_title(title,pad=12)
        if density:
            ax.set_xscale("log")
            ax.set_xticks(x);ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_:f"{v:.3g}"))
            ax.set_xlabel("Actual edge density (%) — log scale")
            ax.set_ylabel("Median runtime (ms)")
        else:
            ax.set_xscale("log",base=2);ax.set_yscale("log")
            ax.set_xticks(x);ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_:str(int(v))))
            ax.set_xlabel("Vertices n — log scale")
            ax.set_ylabel("Median runtime (ms) — log scale")
        ax.grid(True,which="major",alpha=.2)
        ax.legend(frameon=False)

    def speed(ax):
        selected=sorted([r for r in ratios if r["suite"]=="S3_density"],key=lambda r:float(r["actual_density"]))
        x=[100*float(r["actual_density"]) for r in selected]
        y=[float(r["median_ratio"]) for r in selected]
        error=[[float(r["median_ratio"])-float(r["q1_ratio"]) for r in selected],
               [float(r["q3_ratio"])-float(r["median_ratio"]) for r in selected]]
        ax.errorbar(x,y,yerr=error,color="#4F46A5",marker="o",capsize=3,linewidth=1.8,label="Paired ratio")
        ax.axhline(1,color="#546E7A",linestyle="--",linewidth=1,label="Equal time")
        ax.set_xscale("log");ax.set_yscale("log")
        ax.set_xticks(x);ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_:f"{v:.3g}"))
        ax.set_title("Same-graph speed ratio",pad=12)
        ax.set_xlabel("Actual edge density (%) — log scale")
        ax.set_ylabel("Matrix time / heap time — log scale")
        ax.grid(True,which="major",alpha=.2);ax.legend(frameon=False)

    suites={r["suite"] for r in rows}
    if {"S1_sparse","S2_dense","S3_density"} <= suites:
        specs=[("sparse-time-vs-n",lambda ax:times(ax,"S1_sparse","Sparse graphs: m = 4n")),
               ("dense-time-vs-n",lambda ax:times(ax,"S2_dense","Dense graphs: p = 50%")),
               ("density-time",lambda ax:times(ax,"S3_density","Fixed n = 1,000: density sweep",True)),
               ("density-speedup",speed)]
        for name,draw in specs:
            fig,ax=plt.subplots(figsize=(8,5.2));draw(ax);finish(fig)
            save(fig,name,"Measured timings or paired ratios; "+note)
        fig,axes=plt.subplots(2,2,figsize=(14,10))
        for ax,(_,draw) in zip(axes.flat,specs):draw(ax)
        finish(fig);save(fig,"overview","Four main experimental views. "+note)
        fig,axes=plt.subplots(1,2,figsize=(12,4.8))
        sparse=sorted([r for r in rows if r["suite"]=="S1_sparse" and r["algorithm"]=="matrix_array"],key=lambda r:int(r["n"]))
        heap=sorted([r for r in rows if r["suite"]=="S1_sparse" and r["algorithm"]=="list_indexed_heap"],key=lambda r:int(r["n"]))
        axes[0].plot([int(r["n"]) for r in sparse],[float(r["median_matrix_scan_slots"]) for r in sparse],"o-",color=COLORS["matrix_array"],label="Matrix row slots = n²")
        axes[0].plot([int(r["n"]) for r in heap],[float(r["median_adjacency_entries_scanned"]) for r in heap],"o-",color=COLORS["list_indexed_heap"],label="List entries = 2m")
        axes[0].set_xscale("log",base=2);axes[0].set_yscale("log");axes[0].set_xlabel("Vertices n")
        axes[0].set_ylabel("Inspections (different operations)");axes[0].set_title("Sparse graph traversal work")
        dense=sorted([r for r in rows if r["suite"]=="S2_dense" and r["algorithm"]=="list_indexed_heap"],key=lambda r:int(r["n"]))
        axes[1].plot([int(r["n"]) for r in dense],[float(r["median_adjacency_entries_scanned"]) for r in dense],"o-",color="#087F8C",label="List entries = 2m")
        axes[1].plot([int(r["n"]) for r in dense],[float(r["median_heap_decreases"]) for r in dense],"o-",color="#4F46A5",label="Actual decrease-key count q")
        axes[1].set_xscale("log",base=2);axes[1].set_yscale("log");axes[1].set_xlabel("Vertices n")
        axes[1].set_ylabel("Operation count");axes[1].set_title("Dense graph heap work")
        for ax,data in zip(axes,(sparse,dense)):
            ticks=[int(r["n"]) for r in data]
            ax.set_xticks(ticks);ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_:f"{v:g}"))
            ax.grid(True,alpha=.2);ax.legend(frameon=False,fontsize=9)
        fig.tight_layout();save(fig,"operation-counts","Counters explain work; different operation types are not equivalent time units.")
    else:
        fig,ax=plt.subplots(figsize=(9,5.5))
        configurations=sorted({(r["suite"],int(r["n"]),int(r["m"])) for r in rows},key=lambda r:r[1])
        for offset,algorithm in enumerate(COLORS):
            selected=[next(r for r in rows if r["suite"]==suite and int(r["n"])==n and int(r["m"])==m and r["algorithm"]==algorithm) for suite,n,m in configurations]
            x=[i+(-.18 if offset==0 else .18) for i in range(len(selected))]
            ax.bar(x,[float(r["median_ms"]) for r in selected],width=.34,color=COLORS[algorithm],label=LABELS[algorithm])
        ax.set_xticks(range(len(configurations)),[f"n={n}\nm={m}" for _,n,m in configurations])
        ax.set_yscale("log");ax.set_ylabel("Median runtime (ms) — log scale")
        ax.set_title("Pilot: measurement pipeline check");ax.legend(frameon=False);ax.grid(axis="y",alpha=.2)
        finish(fig);save(fig,"pilot-overview","Pilot validation only; not a final performance conclusion.")
    (target/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(f"Created {len(manifest['figures'])} PNG/SVG figures in {target}")


if __name__ == "__main__":
    main()
