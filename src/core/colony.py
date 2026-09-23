from src.core.cell import Cell
import numpy as np
from src.core.cell import Cell
from src.core.cycle import init_cycle
from src.config.base_config import initstate


def init_founder_mother():
    mother = Cell(
        id = 0,
        is_mother=True,
        pos=np.array([0.0,0.0]),
        parent_id=None,
        founder_id=0,
        colony_id=0,
        subcolony_id=0,
        bud_site_angle = np.random.uniform(0, 2 * np.pi)
        
    )


    init_cycle(mother)
    mother.R = mother.R_max
    if mother.cycle_time > 0:
        mother.CI = 1.0 / mother.cycle_time
    mother.R = mother.R_max
    #if mother.bud_scars == None:
        #mother.bud_site_angle = np.random.uniform(0, 2 * np.pi)
    return mother



