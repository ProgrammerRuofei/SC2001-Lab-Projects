"""Shared environment and display helpers for the Project 2 notebook."""

from pathlib import Path
import os
import tempfile
import json
import io
import subprocess
import sys
import hashlib

# Resolve paths after cloning, whether launched from the repo or notebook folder.
def locate_project():
    here = Path.cwd().resolve()
    for base in (here, *here.parents):
        for candidate in (base, base / "project2-dijkstra"):
            if (candidate / "src/dijkstra_matrix.cpp").is_file():
                return candidate
    raise FileNotFoundError("Open this notebook from inside SC2001-Lab-Projects.")

PROJECT = locate_project()
DATA = PROJECT / "results/main-v1"
FIGURES = PROJECT / "figures/main-v1"

os.environ.setdefault("MPLCONFIGDIR", tempfile.mkdtemp(prefix="sc2001-mpl-"))
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, Image, Code, HTML

def display_table(frame, show_index=None, formats=None):
    """Render real HTML cells with explicit contrast in light and dark IDE themes."""
    import re
    if show_index is None:
        show_index = bool(frame.index.name)
    markup = frame.to_html(index=show_index, border=0, escape=True,
                           formatters=formats, max_rows=None, max_cols=None)
    cell_style = ("color:#172b4d !important; border:1px solid #cbd5e1; "
                  "padding:9px 12px; font-size:14px; line-height:1.5; "
                  "font-variant-numeric:tabular-nums; vertical-align:top;")
    def style_cell(match):
        tag, attributes = match.groups()
        background = "#e8eef5" if tag == "th" else "#ffffff"
        weight = "700" if tag == "th" else "400"
        return (f'<{tag}{attributes} style="{cell_style} '
                f'background-color:{background} !important; font-weight:{weight};">')
    markup = re.sub(r"<(th|td)([^>]*)>", style_cell, markup)
    markup = markup.replace('<table ', '<table style="border-collapse:collapse; '
                            'font-family:system-ui,sans-serif; color:#172b4d; '
                            'background-color:#ffffff; margin:0;" ', 1)
    display(HTML('<div style="background-color:#ffffff; color:#172b4d; '
                 'padding:12px; overflow-x:auto; border-radius:6px; '
                 'border:1px solid #cbd5e1;">' + markup + '</div>'))

def display_plot(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    display(Image(data=buffer.getvalue(), width=1000))

pd.set_option("display.max_rows", 30)
pd.set_option("display.max_columns", 12)
print("Project located; archived experiment: main-v1")
print("Python", sys.version.split()[0], "| pandas", pd.__version__, "| Matplotlib", matplotlib.__version__)
