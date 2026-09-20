from typing import Tuple
from config.base_config import ModelParams
import math

# A 2D vector type for readability
Vector = Tuple[float, float]


def distance_and_direction(ci: Vector, cj: Vector) -> tuple[float, Vector, Vector]:
    """Return distance dij, vector rij = ci - cj, and unit vector nij.

    ci, cj are 2D positions (x, y).
    """
    rij = (ci[0] - cj[0], ci[1] - cj[1])
    dij = math.hypot(rij[0], rij[1])
    if dij == 0.0:
        # If they are exactly on top of each other, avoid division by zero
        nij = (0.0, 0.0)
    else:
        nij = (rij[0] / dij, rij[1] / dij)
    return dij, rij, nij


# Effective modulus, same idea as your Eij_tilde
EIJ_TILDE = (3.0 / 2.0) * (1.0 - ModelParams.sigma**2) / ModelParams.E


def repulsive_force(ci: Vector, cj: Vector, Ri: float, Rj: float) -> Vector:
    """Simple repulsive force between overlapping cells i and j.

    - If the cells do not overlap, return (0, 0).
    - If they overlap, use a Hertz-like contact model (your original formula idea).
    """
    dij, _, nij = distance_and_direction(ci, cj)

    if dij == 0.0:
        # Degenerate case: put no force for now
        return (0.0, 0.0)

    overlap = Ri + Rj - dij
    if overlap <= 0.0:
        # No overlap → no contact force
        return (0.0, 0.0)

    # Magnitude of gradient of repulsive energy (up to constant factors)
    scalar_grad = - (overlap ** 1.5) / (2.0 * EIJ_TILDE) * math.sqrt((Ri * Rj) / (Ri + Rj))

    # Force on cell i is minus gradient wrt ci; we approximate that with this:
    Fx = scalar_grad * nij[0]
    Fy = scalar_grad * nij[1]
    return (Fx, Fy)

def mother_bud_spring_force(cm, cb, Rm, Rb):
     d_mb, _, n_mb = distance_and_direction(cm, cb)

     stretch = d_mb - (Rm + Rb)

     F = -(2 * ModelParams.Kbud * stretch)
     Fx = F * n_mb[0]
     Fy = F * n_mb[1]
     return (Fx, Fy)