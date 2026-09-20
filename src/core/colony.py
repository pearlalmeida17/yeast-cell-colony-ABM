from core.cell import Cell
import numpy as np
from .cell import Cell
from .cycle import init_cycle


def init_founder_mother():
    mother = Cell(
        id_=0,
        is_mother=True,
        pos=np.array([0.0,0.0]),
        parent_id=None,
        founder_id=0,
        colony_id=0,
        subcolony_id=0
        
    )


    init_cycle(mother)
    mother.R = mother.R_max
    if mother.bud_scars == None:
        mother.bud_site_angle = np.random.uniform(0, 2 * np.pi)
    return mother



