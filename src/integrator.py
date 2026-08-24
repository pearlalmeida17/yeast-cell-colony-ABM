from typing import Tuple, List
from config import initstate, ModelParams, simulparams
from scipy.spatial import KDTree
import numpy as np
from forces import repulsive_force

Vector = Tuple[float, float]


def step_positions(centers: List[Vector], cells: List) -> List[Vector]:
    """Take one overdamped step in time for all cells.

    We use a simple rule:
        x_{t+dt} = x_t - (dt / (eta * (1 + R/2))) * F

    for each cell, where F is the net force on that cell.
    """
    
    radii_list = [cell.radius for cell in cells]
    
    centers_array = np.array(centers)
    tree = KDTree(centers_array)


    new_centers: List[Vector] = []

    for i in range(len(centers)):

        Fx, Fy = 0.0, 0.0
        ci = centers_array[i]
        neighbors = tree.query_ball_point(centers_array[i], 6.0)

       
        neighbors = [j for j in neighbors if j != i]

        

        for j in neighbors:    
            fx, fy = repulsive_force(ci, centers_array[j], radii_list[i], radii_list[j])
            Fx += fx
            Fy += fy
        
        
        mobility = simulparams.dt / (ModelParams.eta * (1.0 + radii_list[i] / 2.0))
        dx = -mobility * Fx
        dy = -mobility * Fy
        new_centers.append((ci[0] + dx, ci[1] + dy))

    return new_centers