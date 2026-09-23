from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Iterable

import pyarrow as pa
import pyarrow.parquet as pq

from src.storage.schema import birth_record, cell_record


class SimulationStore:
    """Buffered Parquet writer for one simulation run."""

    def __init__(self, root="data/runs", run_id=None, metadata=None):
        self.run_id = run_id or f"run_{uuid.uuid4().hex[:10]}"
        self.run_dir = Path(root) / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.snapshot_dir = self.run_dir / "snapshots"
        self.snapshot_dir.mkdir(exist_ok=True)
        self.births = []
        self.events = []
        self.snapshot_parts = 0
        self.metadata = metadata or {}
        (self.run_dir / "metadata.json").write_text(
            json.dumps({"run_id": self.run_id, **self.metadata}, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _write_rows(rows, path):
        if rows:
            pq.write_table(pa.Table.from_pylist(rows), path, compression="zstd")

    def record_birth(self, cell):
        self.births.append(birth_record(cell, self.run_id))

    def record_event(self, event):
        self.events.append(event)

    def record_snapshot(self, cells: Iterable, time: float):
        rows = [cell_record(cell, self.run_id, time) for cell in cells]
        path = self.snapshot_dir / f"part-{self.snapshot_parts:06d}.parquet"
        self._write_rows(rows, path)
        self.snapshot_parts += 1

    def flush(self):
        if self.births:
            self._write_rows(self.births, self.run_dir / "cell_births.parquet")
            self.births.clear()
        if self.events:
            self._write_rows(self.events, self.run_dir / "events.parquet")
            self.events.clear()

    def save_checkpoint(self, cells: Iterable, time: float):
        path = self.run_dir / f"checkpoint_{time:.3f}.parquet"
        self._write_rows([cell_record(c, self.run_id, time) for c in cells], path)
        return path

    def close(self):
        self.flush()