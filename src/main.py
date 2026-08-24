from typing import Dict, List, Tuple

import numpy as np

from config import initstate, simulparams
from integrator import step_positions

Vector = Tuple[float, float]


def run_simulation() -> Dict[int, np.ndarray]:
    """Run the cell simulation and return positions over time.

    Returns
    -------
    positions : dict
        keys are cell indices (0, 1, 2, ...)
        values are arrays of shape (timesteps, 2) with (x, y) positions.
    """
    num_cells = len(initstate.cell_centers)
    timesteps = int(simulparams.total_time / simulparams.dt)

    # Initialize positions dict: positions[i][t] = (x, y)
    positions: Dict[int, np.ndarray] = {
        i: np.zeros((timesteps, 2), dtype=float) for i in range(num_cells)
    }

    # Set t = 0 from initstate
    centers: List[Vector] = []
    for i in range(num_cells):
        x, y = initstate.cell_centers[i]
        positions[i][0, 0] = x
        positions[i][0, 1] = y
        centers.append((x, y))

    # Time stepping loop
    for t in range(1, timesteps):
        centers = step_positions(centers)
        for i, (x, y) in enumerate(centers):
            positions[i][t, 0] = x
            positions[i][t, 1] = y

    return positions


if __name__ == "__main__":
    positions = run_simulation()
    print("Final positions:")
    for i, traj in positions.items():
        print(f"Cell {i}: {traj[-1]}")