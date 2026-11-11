"""Draws the figures for the slides from the CSV files written by knapsack.cpp,
and prints the fitted lines.

Run after the C++ program:   python plot.py > results/fit.txt

  figures/subproblem_graph_P15.png   question (2): subproblem graph of P(15)
  figures/time_vs_C.png              experiment 2: time against C
  figures/time_vs_n.png              experiment 3: time against n
  figures/naive_vs_dp.png            experiment 4: plain recursion against the DP
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BLUE, ORANGE, GREEN = "#2a78d6", "#eb6834", "#1baf7a"
INK, GRAY, BACKGROUND = "#18212b", "#6b7380", "#f4f2ec"

# A figure of width 10 inches is shown 1000 px wide on the 1920 x 1080 slides.
plt.rcParams.update({
    "font.family": "Segoe UI",
    "font.size": 18,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "figure.facecolor": BACKGROUND,
    "axes.facecolor": BACKGROUND,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#dedad0",
})
os.makedirs("figures", exist_ok=True)


def fit_line(x, y):
    """Least-squares line y = a*x + b, and its R^2."""
    a, b = np.polyfit(x, y, 1)
    r2 = 1 - np.sum((y - (a * x + b)) ** 2) / np.sum((y - np.mean(y)) ** 2)
    return a, b, r2


def plot_linear(x, y, a, b, xlabel, filename):
    """Measured times and the fitted line."""
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.plot(x, a * x + b, "--", color=GRAY, lw=2, label="fitted line")
    ax.plot(x, y, "o", color=BLUE, ms=11, label="measured (median of 5 runs)")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("time (ms)")
    ax.set_ylim(0, max(y) * 1.12)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(filename, dpi=200)


def readable_time(ms, position=None):
    """Axis label for a time given in ms: 10 µs, 1 ms, 1 s, ..."""
    if ms >= 1000:
        return f"{ms / 1000:g} s"
    if ms >= 1:
        return f"{ms:g} ms"
    return f"{ms * 1000:g} µs"


# ---- Question (2): subproblem graph of P(15) with w = (4, 5, 8) ----
# Built from the recursive definition: P(c) needs P(c - w[i]) for every type i with w[i] <= c.
w = [4, 5, 8]
nodes, edges, todo = {15}, [], [15]
while todo:
    c = todo.pop()
    for i in range(len(w)):
        if w[i] <= c:
            edges.append((c, c - w[i], i))
            if c - w[i] not in nodes:
                nodes.add(c - w[i])
                todo.append(c - w[i])
print(f"Subproblem graph of P(15): {len(nodes)} nodes {sorted(nodes, reverse=True)}, {len(edges)} edges")

# Layout: every node is c = 15 - 4a - 5b (a steps of weight 4, b steps of weight 5;
# a step of weight 8 is two steps of weight 4). Row a + b, column b - a.
position = {}
for a in range(4):
    for b in range(4):
        if 15 - 4 * a - 5 * b in nodes:
            position[15 - 4 * a - 5 * b] = (1.25 * (b - a), -1.3 * (a + b))

fig, ax = plt.subplots(figsize=(11, 6.2))
for c, d, i in edges:
    curve = "arc3,rad=0.4" if i == 2 else "arc3,rad=0"     # weight-8 edges bend around a node
    ax.annotate("", xy=position[d], xytext=position[c],
                arrowprops=dict(arrowstyle="-|>", color=[BLUE, ORANGE, GREEN][i], lw=2.6,
                                mutation_scale=24, shrinkA=27, shrinkB=29, connectionstyle=curve))
for c, (x, y) in position.items():
    is_base_case = all(wi > c for wi in w)
    ax.scatter(x, y, s=2700, color="#dcd8cc" if is_base_case else "#fbfaf6",
               edgecolors=INK, linewidths=2, zorder=3)
    ax.text(x, y, str(c), ha="center", va="center", fontsize=24, fontweight="bold", zorder=4)
ax.set_xlim(-4.3, 4.3)
ax.set_ylim(-4.35, 0.45)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout(pad=0.2)
fig.savefig("figures/subproblem_graph_P15.png", dpi=200)

# ---- Experiment 2: time against C (n = 100) ----
d = pd.read_csv("results/time_vs_C.csv")
a, b, r2 = fit_line(d.C, d.time_ms)
print(f"Experiment 2 (n = 100): {a * 100000:.2f} ms per 100,000 of C, intercept {b:.2f} ms, "
      f"R^2 = {r2:.4f}, {a * 1e6 / 100:.3f} ns per step")
plot_linear(d.C / 1000, d.time_ms, a * 1000, b, "capacity C (thousands)", "figures/time_vs_C.png")

# ---- Experiment 3: time against n (C = 100,000) ----
d = pd.read_csv("results/time_vs_n.csv")
a, b, r2 = fit_line(d.n, d.time_ms)
print(f"Experiment 3 (C = 100,000): {a * 100:.2f} ms per 100 types, intercept {b:.2f} ms, "
      f"R^2 = {r2:.4f}, {a * 1e6 / 100000:.3f} ns per step")
plot_linear(d.n, d.time_ms, a, b, "number of types n", "figures/time_vs_n.png")

# ---- Experiment 4: plain recursion against the DP (w = 4, 5, 8) ----
d = pd.read_csv("results/naive_vs_dp.csv")
growth_time = np.exp(np.polyfit(d.C, np.log(d.naive_ms), 1)[0])
growth_calls = np.exp(np.polyfit(d.C, np.log(d.naive_calls), 1)[0])
# Theory: the number of calls grows like x^C, where x^-4 + x^-5 + x^-8 = 1, i.e. x^8 - x^4 - x^3 - 1 = 0.
roots = np.roots([1, 0, 0, 0, -1, -1, 0, 0, -1])
x = max(r.real for r in roots if abs(r.imag) < 1e-9)
last = d.iloc[-1]
print(f"Experiment 4: plain recursion grows by x{growth_time:.3f} (time) and x{growth_calls:.3f} (calls) "
      f"per unit of C; theory x{x:.4f}")
print(f"  C = {int(last.C)}: plain recursion {int(last.naive_calls):,} calls, {last.naive_ms:.0f} ms; "
      f"DP {last.dp_ms * 1000:.2f} us")

fig, ax = plt.subplots(figsize=(10, 6.2))
ax.semilogy(d.C, d.naive_ms, "o-", color=ORANGE, lw=2.6, ms=9, label="plain recursion (no table)")
ax.semilogy(d.C, d.dp_ms, "o-", color=BLUE, lw=2.6, ms=9, label="bottom-up DP")
ax.text(last.C, last.naive_ms * 2.2, f"{last.naive_ms / 1000:.1f} s", ha="right", va="bottom")
ax.text(last.C, last.dp_ms * 2.2, f"{last.dp_ms * 1000:.2f} µs", ha="right", va="bottom")
ax.yaxis.set_major_formatter(plt.FuncFormatter(readable_time))
ax.set_ylim(5e-5, 2e4)
ax.set_xlabel("capacity C")
ax.set_ylabel("time (log scale)")
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig("figures/naive_vs_dp.png", dpi=200)
