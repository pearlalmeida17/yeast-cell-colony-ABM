from __future__ import annotations

import argparse
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from src.analysis.export import export_excel
from src.analysis.metrics import calculate_all_metrics
from src.analysis.plots import plot_paper_metrics
from src.storage.loaders import load_run_records


def analyze_run(run_dir: str):
    run_dir = Path(run_dir)
    records = load_run_records(run_dir)
    metrics = calculate_all_metrics(records["snapshots"])
    pq.write_table(pa.Table.from_pylist(metrics), run_dir / "metrics.parquet", compression="zstd")
    export_excel(run_dir, metrics)
    figure = plot_paper_metrics(metrics)
    figure.savefig(run_dir / "paper_metrics.png", dpi=160, bbox_inches="tight")
    print(f"Metrics written to: {run_dir / 'metrics.parquet'}")
    print(f"Excel report written to: {run_dir / 'report.xlsx'}")
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a stored yeast-colony simulation run")
    parser.add_argument("run_dir", help="Example: data/runs/run_1234567890")
    args = parser.parse_args()
    analyze_run(args.run_dir)