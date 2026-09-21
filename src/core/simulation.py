import numpy as np
from src.config.base_config import initstate, simulparams
from src.core.colony import init_founder_mother
from src.core.environment import build_subdomains, compute_biomass, update_GRadjust, apply_nutrient_limitation
from src.core.mechanics import compute_forces_with_subdomains
from src.core.rules import apply_cell_rules
from src.core.lineage import Lineage
from src.core.cycle import update_CP

def run_simulation():
    cells = []
    
    mother = init_founder_mother()
    cells.append(mother)
    next_id = 1

    GRadjust = {}  # per-subdomain growth-rate adjustment

    t = 0.0
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
            update_CP(cell, simulparams.dt)
            apply_cell_rules(cell, simulparams.dt, new_cells)

        my_lineage = Lineage()

        # assign IDs and lineage
        for daughter in new_cells:
            daughter.id = next_id
            next_id += 1
            my_lineage.add_edge(daughter.parent_id, daughter.id)

        cells.extend(new_cells)

        # mechanics
        compute_forces_with_subdomains(cells, subdomains, simulparams.dt)

        t += simulparams.dt

        # optional: logging, snapshots, metrics

    return cells, Lineage
