from config.base_config import ModelParams
from forces import repulsive_force, mother_bud_spring_force
import numpy as np



NEIGHBOR_OFFSETS = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (0,0), (1, 0),
    (-1, 1), (0, 1), (1, 1),
]

def get_neighbor_indices(idx):
    i, j = idx
    return [(i+di, j+dj) for di, dj in NEIGHBOR_OFFSETS]

def compute_forces_with_subdomains(cells, subdomains, dt):

    forces = {cell.id: np.zeros(2) for cell in cells}

    for idx, cell_list in subdomains.items():
        neighbor_idxs = get_neighbor_indices(idx)

        neighbor_cells = []
        for nidx in neighbor_idxs:
            neighbor_cells.extend(subdomains.get(nidx, []))

        for ci in cell_list:
            for cj in neighbor_cells:
                if cj.id <= ci.id:
                    continue

                repulsive_force_on_ci = repulsive_force(np.squeeze(ci.pos), np.squeeze(cj.pos), ci.R, cj.R )
                if cell.has_bud or cell.bud is not None:
                    mother_bud_force = mother_bud_spring_force(np.squeeze(ci.pos), np.squeeze(cell.bud["pos"]), ci.R, ci.bud["R"] )
                else:
                    mother_bud_force = 0

                total_force = (repulsive_force_on_ci[0] + mother_bud_force[0], repulsive_force_on_ci[1] + mother_bud_force[1])

                fx, fy = total_force
                ax, ay = forces[ci.id]
                bx, by = forces[cj.id]

                forces[ci.id] = (ax + fx, ay + fy)
                forces[cj.id] = (bx - fx, by - fy)

            
    for cell in cells:

        fx, fy = forces[cell.id]
        x, y = cell.pos
        coeff = (dt/(ModelParams.eta)(1 + cell.R/2))

        cell.pos = (x - fx * coeff, y - fy * coeff) 
        
                
                                  