import math
from collections import defaultdict
from src.config.base_config import initstate,simulparams

def get_subdomain_index(pos):
    i = int(math.floor(pos[0] / initstate.di_t))
    j = int(math.floor(pos[1] / initstate.di_t))
    return (i, j)

def build_subdomains(cells):
    subdomains = defaultdict(list)

    for cell in cells:
        idx = get_subdomain_index(cell.pos)
        cell.subdomain_idx = idx
        subdomains[idx].append(cell)
    return subdomains

def compute_biomass(subdomains):
    biomass = {}
    for idx, cell_list in subdomains.items():
        total = 0.0
        for cell in cell_list:
            total += math.pi * (cell.R ** 2)
        biomass[idx] = total
    
    return biomass

def update_GRadjust(GRadjust, biomass, dt):
    new = {}
    for idx, Mj in biomass.items():
        Mj_div =  min(Mj / initstate.Mjmax, 1.0)
        prev = GRadjust.get(idx, 1.0)
        updated = prev - simulparams.r * Mj_div * dt
        new[idx] = max(updated, 0.0)
    return new

def apply_nutrient_limitation(cells, GRadjust):
    if not initstate.NUTRIENT_LIMITED:
        return
    for cell in cells:
        idx = cell.subdomain_idx
        factor = GRadjust.get(idx, 1.0)
        cell.CI = cell.CI_original * factor


def get_colony_radius(cells):
    furthest_cell = max(cells, key = lambda c : math.hypot(c.pos[0], c.pos[1]))
    colony_radius = math.hypot(furthest_cell.pos[0], furthest_cell.pos[1])
    return  colony_radius

def nutrient_factor(cell, cells, nutrient_limited):
    if not nutrient_limited:
        return 1.0
    else:
        colony_radius = get_colony_radius(cells)
        distance = math.hypot(cell.pos[0], cell.pos[1])

        nutrient_factor = distance/colony_radius

        return nutrient_factor