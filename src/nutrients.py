import math

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