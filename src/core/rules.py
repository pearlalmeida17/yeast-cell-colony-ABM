from src.core.cycle import grow_radius
from src.core.budding import maybe_start_bud, update_bud, handle_non_budding_divison

def apply_cell_rules(cell, dt, new_cells):
    
    grow_radius(cell, dt)

    #budding mode
    if cell.has_bud:
        daughter = update_bud(cell, dt)
        if daughter is not None:
            new_cells.append(daughter)
    else:
        maybe_start_bud(cell)


    #non-budding mode
    daughter_nb = handle_non_budding_divison(cell)
    if daughter_nb is not None:
        new_cells.append(daughter_nb)
