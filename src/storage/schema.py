from __future__ import annotations

from typing import Any

def cell_record(cell: Any, run_id: str, time: float) -> dict[str, Any]:
    bud = cell.bud or {}
    bud_pos = bud.get("pos", (None,None))
    return{
        "run_id" : run_id,
        "time": float(time),
        "cell_id": int(cell.id),
        "parent_id": None if cell.parent_id is None else int(cell.parent_id),
        "founder_id": None if cell.founder_id is None else int(cell.founder_id),
        "subcolony_id": None if cell.subcolony_id is None else int(cell.subcolony_id),
        "x": float(cell.pos[0]), "y": float(cell.pos[1]),
        "R": float(cell.R), "R_max": float(cell.R_max),
        "CP": float(cell.CP), "CI": float(cell.CI),
        "is_mother": bool(cell.is_mother), 
        "has_bud": bool(cell.has_bud),
        "bud_x": None if bud_pos[0] is None else float(bud_pos[0]),
        "bud_y": None if bud_pos[1] is None else float(bud_pos[1]),
        "bud_R": None if bud.get("R") is None else float(bud["R"]),
        "subdomain_i": None if cell.subdomain_idx is None else int(cell.subdomain_idx[0]),
        "subdomain_j": None if cell.subdomain_idx is None else int(cell.subdomain_idx[1]),
        "birth_time": float(getattr(cell, "birth_time", 0.0)),
        "birth_x": float(getattr(cell, "birth_pos", cell.pos)[0]),
        "birth_y": float(getattr(cell, "birth_pos", cell.pos)[1]),
    }

def birth_record(cell: Any, run_id: str) -> dict[str, Any]:
    return {
        "run_id": run_id, "cell_id": int(cell.id),
        "parent_id": None if cell.parent_id is None else int(cell.parent_id),
        "founder_id": None if cell.founder_id is None else int(cell.founder_id),
        "subcolony_id": None if cell.subcolony_id is None else int(cell.subcolony_id),
        "birth_time": float(getattr(cell, "birth_time", 0.0)),
        "birth_x": float(getattr(cell, "birth_pos", cell.pos)[0]),
        "birth_y": float(getattr(cell, "birth_pos", cell.pos)[1]),
        "R_max": float(cell.R_max),
        "is_mother_at_birth": bool(cell.is_mother),
    }

def event_record(run_id: str, time: float, event_type: str, **values: Any) -> dict[str, Any]:
    return {
        "run_id": run_id, 
        "time": float(time), 
        "event_type": event_type,
        "cell_id": values.get("cell_id"), 
        "parent_id": values.get("parent_id"),
        "daughter_id": values.get("daughter_id"), 
        "x": values.get("x"),
        "y": values.get("y"),
    }
