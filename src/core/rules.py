from src.core.cycle import grow_radius
from src.core.budding import maybe_start_bud, update_bud, handle_non_budding_divison

def apply_cell_rules(cell, dt, new_cells):
    update_bud(cell, dt)
    grow_radius(cell, dt)

    #budding mode
    maybe_start_bud(cell)
    daughter = update_bud(cell, dt)
    if daughter is not None:
        new_cells.append(daughter)

    #non-budding mode
    daughter_nb = handle_non_budding_divison(cell)
    if daughter_nb is not None:
        new_cells.append(daughter_nb)
