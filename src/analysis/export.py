from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.storage.loaders import load_run_records


def export_excel(run_dir, metrics, output_path=None):
    run_dir = Path(run_dir)
    output_path = Path(output_path or run_dir / "report.xlsx")
    records = load_run_records(run_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pd.DataFrame(metrics).to_excel(writer, sheet_name="Metrics", index=False)
        pd.DataFrame(records["births"]).to_excel(writer, sheet_name="Cell births", index=False)
        pd.DataFrame(records["events"]).to_excel(writer, sheet_name="Events", index=False)
        pd.DataFrame([records["metadata"]]).to_excel(writer, sheet_name="Metadata", index=False)
    return output_path
