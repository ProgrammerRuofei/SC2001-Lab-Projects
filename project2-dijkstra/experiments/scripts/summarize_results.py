"""Member C: validate and aggregate per graph, then per configuration. Scaffold only; no measurements or charts are produced."""
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Member C: validate and aggregate per graph, then per configuration')
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.parse_args()
    # TODO: implement the steps and output schema in docs/execution-plan.md.
    parser.exit(2, "PENDING: implement this script before collecting or analyzing data.\n")

if __name__ == "__main__":
    main()
