"""Exercise public input handling; accepts an explicit pending solver state."""
import subprocess
import sys

binary = sys.argv[1]


def run(*args):
    return subprocess.run([binary, *args], capture_output=True, text=True, check=False)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


for args in [(), ("--help",)]:
    result = run(*args)
    require(result.returncode == 0 and "Unbounded Knapsack" in result.stdout, "Help failed")

invalid_cases = [
    ("--case",), ("--case", "unknown"), ("--unknown",), ("--table",),
    ("--case", "a", "--case", "b"), ("--case", "a", "--capacity", "3"),
    ("--capacity", "1", "--weights", "2,3", "--profits", "4"),
    ("--capacity", "-1", "--weights", "2", "--profits", "4"),
    ("--capacity", "2x", "--weights", "2", "--profits", "4"),
    ("--capacity", "2", "--weights", "0", "--profits", "4"),
    ("--capacity", "2", "--weights", "2,", "--profits", "4,5"),
    ("--capacity", "2", "--weights", "", "--profits", "4"),
]
for args in invalid_cases:
    result = run(*args)
    require(result.returncode == 1 and "ERROR:" in result.stderr, f"Bad input accepted: {args}")

valid_cases = [
    (("--case", "a", "--table"), 28),
    (("--case", "b"), 16),
    (("--case", "graph"), 21),
    (("--capacity", "0", "--weights", "4", "--profits", "7"), 0),
]
pending = 0
for args, expected in valid_cases:
    result = run(*args)
    if result.returncode == 2:
        pending += 1
        require("PENDING:" in result.stderr and "maximum_profit=" not in result.stdout,
                "Pending solver must not print a computed answer")
    else:
        require(result.returncode == 0 and f"maximum_profit={expected}\n" in result.stdout,
                f"Unexpected result for {args}: {result.stdout} {result.stderr}")

print(f"PASS: CLI handling ({pending} valid requests report solver PENDING)")
