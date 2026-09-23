from __future__ import annotations

import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from src.core.cell import Cell
from src.core.cycle import init_cycle


def _read_rows(path: Path):
    return pq.read_table(path).to_pylist() if path.exists() else []


def write_initial_cells(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), path, compression="zstd")


def ensure_founder_file(path, radius=2.58):
    path = Path(path)
    
    if not path.exists() or path.stat().st_size == 0:
        write_initial_cells(path, [{
            "id": 0, "parent_id": None, "founder_id": 0,
            "x": 0.0, "y": 0.0, "R": radius,
            "is_mother": True, "subcolony_id": 0,
        }])
    return path


def load_initial_cells(path):
    rows = _read_rows(Path(path))
    if not rows:
        raise ValueError(f"Initial-cell file is empty: {path}")
    cells = []
    for row in rows:
        cell = Cell(
            id=int(row["id"]), is_mother=bool(row.get("is_mother", True)),
            pos=(float(row["x"]), float(row["y"])),
            parent_id=row.get("parent_id"),
            founder_id=row.get("founder_id", row["id"]),
            subcolony_id=row.get("subcolony_id"),
            birth_time=float(row.get("birth_time", 0.0)),
        )
        cell.R = float(row.get("R", cell.R_max))
        init_cycle(cell)
        cells.append(cell)
    return cells


def load_run_records(run_dir):
    run_dir = Path(run_dir)
    snapshots = []
    for path in sorted((run_dir / "snapshots").glob("*.parquet")):
        snapshots.extend(_read_rows(path))
    metadata_path = run_dir / "metadata.json"
    return {
        "metadata": json.loads(metadata_path.read_text()) if metadata_path.exists() else {},
        "births": _read_rows(run_dir / "cell_births.parquet"),
        "events": _read_rows(run_dir / "events.parquet"),
        "snapshots": snapshots,
    }