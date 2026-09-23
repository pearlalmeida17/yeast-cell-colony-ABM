import random
import numpy as np
from pathlib import Path
from src.config.base_config import initstate, simulparams
from src.core.environment import build_subdomains, compute_biomass, update_GRadjust, apply_nutrient_limitation
from src.core.mechanics import compute_forces_with_subdomains
from src.core.rules import apply_cell_rules
from src.core.lineage import Lineage
from src.core.cycle import update_CP
from src.storage.loaders import ensure_founder_file, load_initial_cells
from src.storage.parquet_store import SimulationStore
from src.storage.schema import event_record

def run_simulation(initial_cells_path = "data/inputs/initial_cells.parquet", output_dir = "data/runs", run_id=None, seed=None, snapshot_interval=15.0, checkpoint_interval=None, record=True):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    initial_cells_path = ensure_founder_file(initial_cells_path, simulparams.R_avg)
    cells = load_initial_cells(initial_cells_path)
    next_id = max((cell.id for cell in cells), default=-1) + 1
    

    GRadjust = {}  # per-subdomain growth-rate adjustment

    t = 0.0
    lineage = Lineage()

    metadata = {
        "seed" : seed,
        "total_time": simulparams.total_time,
        "dt": simulparams.dt,
        "budding": initstate.BUDDING,
        "nutrient_limited": initstate.NUTRIENT_LIMITED,
        "initial_cells_path": str(initial_cells_path),
    }

    store = SimulationStore(output_dir, run_id, metadata) if record else None
    if store:
        for cell in cells:
            for cell in cells:
                store.record_birth(cell)
            store.record_snapshot(cells, 0.0)

    next_snapshot = snapshot_interval
    next_checkpoint = checkpoint_interval if checkpoint_interval else None


    while t < simulparams.total_time:
        # spatial subdomains
        subdomains = build_subdomains(cells)

        # nutrient-limited growth
        if initstate.NUTRIENT_LIMITED:
            biomass = compute_biomass(subdomains)
            GRadjust = update_GRadjust(GRadjust, biomass, simulparams.dt)
            apply_nutrient_limitation(cells, GRadjust)

        # cell rules (CP, growth, budding/non-budding)
        new_cells = []
        for cell in cells:
            lineage.register_initial_cell(cell)
            update_CP(cell, simulparams.dt)
            apply_cell_rules(cell, simulparams.dt, new_cells)

        

        # assign IDs and lineage
        for daughter in new_cells:
            daughter.id = next_id
            next_id += 1
            daughter.birth_time = t
            daughter.birth_pos = daughter.pos.copy()
            lineage.add_edge(daughter.parent_id, daughter.id)
            if store:
                store.record_birth(daughter)
                store.record_event(event_record(
                    store.run_id, t, "daughter_created",
                    cell_id=daughter.id, parent_id=daughter.parent_id, 
                    daughter_id=daughter.id, x=daughter.pos[0], y=daughter.pos[1]
                ))

        cells.extend(new_cells)

        # mechanics
        compute_forces_with_subdomains(cells, subdomains, simulparams.dt)

        t += simulparams.dt
        if store and t + 1e-9 >= next_snapshot:
            store.record_snapshot(cells, t)
            next_snapshot += snapshot_interval
        if store and next_checkpoint is not None and t + 1e-9 >= next_checkpoint:
            store.save_checkpoint(cells, t)
            next_checkpoint += checkpoint_interval

    if store:
        store.record_snapshot(cells, simulparams.total_time)
        store.close()

    return cells, lineage, store.run_id if store else None
