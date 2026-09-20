import numpy as np
from config.base_config import cellcycle


def init_cycle(cell):
    if cell.is_mother:
        cell.G1 = (1 + np.random.uniform(-0.1, 0.1)) * cellcycle.G1avgmother
    else:
        cell.G1 = (1 + np.random.uniform(-0.1, 0.1)) * cellcycle.G1avgdaughter


    
    cell.G2 = (1 + np.random.uniform(-0.1, 0.1)) * cellcycle.G2avg
    cell.cycle_time = cell.G1 + cell.G2
    cell.CI_original = 1.0 / cell.cycle_time
    cell.CI = cell.CI_original
    cell.R = 0.0 if not cell.is_mother else cell.R_max

def in_G1(cell):
        return cell.CP * cell.cycle_time < cell.G1

def update_CP(cell, dt):
        cell.CP += cell.CI * dt

def grow_radius(cell, dt):
    if cell.in_G1() and cell.R < cell.R_max:
        growth_rate = cell.R_max/ cell.G1
        cell.R = min(cell.R + cell.grow_radius*dt , cell.R_max)





