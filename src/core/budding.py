import random, math
from src.core.cycle import init_cycle, in_G1
from src.core.cell import Cell
from src.config.base_config import initstate
from src.core.lineage import Lineage
import numpy as np



def choose_bud_site_angle(cell):
    # No Budding scar yet; only 1 scar from the mother; hence, a daughter cell's first bud
    scars = cell.bud_scars
    
    if len(scars) == 0:
        angle = random.uniform(0.0, 2.0 * math.pi)
    elif  len(scars) == 1:
        angle = (scars[-1] + math.pi ) % (2 * math.pi)
    else:    
        if random.random() < 0.5:
            angle = (scars[-1] + math.pi ) % (2 * math.pi)
        else:
            angle_offset = math.radians(random.uniform(-10, 10))
            angle = (scars[-1] + angle_offset) % (2 * math.pi)

    while any(abs(angle - scar) < 1e-8 for scar in scars):
        angle = (angle + math.radians(10)) % (2.0 * math.pi)
        
    if angle in cell.bud_scars:
        return choose_bud_site_angle(cell)
    else:
         
        cell.bud_site_angle = angle #angle is in radians

        return angle
    


def maybe_start_bud(cell):
    if not initstate.BUDDING:
        return
    if not in_G1(cell) and not cell.has_bud:
        if not cell.is_mother:
            init_cycle(cell)
            cell.is_mother = True

        cell.has_bud = True
        cell.bud_age = 0.0

        if cell.bud_site_angle is None:
            cell.bud_site_angle = choose_bud_site_angle(cell)

        cell.bud = {
            "R" : 0.0,
            "angle" : cell.bud_site_angle,
            "pos": tuple(cell.pos),

        }


def create_daughter_from_bud(cell):

    birth_scar = (cell.bud["angle"] + math.pi) % (2* math.pi)

    daughter = Cell(
        id = None,
        is_mother = False,
        pos = cell.bud["pos"],
        parent_id=cell.id,
        founder_id=cell.founder_id if cell.founder_id is not None else cell.id,
        colony_id=cell.colony_id,
        subcolony_id=cell.subcolony_id,
        bud_scars=[birth_scar]
        
    )
    
    init_cycle(daughter)
    if daughter.cycle_time > 0:
        daughter.CI = 1.0 / daughter.cycle_time

    lineage_ins = Lineage()
    lineage_ins.update_ids(daughter)

    #what happens to cell.bud_site_angle after creation of daughter cell
    cell.bud_site_angle = None
    cell.bud_scars.append(cell.bud["angle"])
    cell.is_mother = True
    cell.CP = 0.0
    init_cycle(cell)
    cell.R = cell.R_max
    return daughter



def update_bud( cell,dt,):
    if not initstate.BUDDING or not cell.has_bud:
        return None

    bud_attach_time = cell.G2
    bud_growth_rate = initstate.Ravg/ bud_attach_time

    cell.bud_age += dt
    cell.bud["R"] += bud_growth_rate * dt

    if cell.bud_site_angle is None:
        maybe_start_bud(cell)

    ux = np.cos(cell.bud["angle"])
    uy = np.sin(cell.bud["angle"])
    direction = np.array([ux,uy])

    cell.bud["pos"] = cell.pos + (cell.R + cell.bud["R"]) * direction

    if cell.bud_age >= bud_attach_time:
        daughter = create_daughter_from_bud(cell)
        cell.has_bud = False
        cell.bud = None
        cell.bud_age = 0.0
        return daughter

    return None

def handle_non_budding_divison(cell):
    if initstate.BUDDING:
        return None
    if cell.CP < 1.0:
        return None

    cell.is_mother = True
    init_cycle(cell)
    
    daughter_pos = cell.pos + np.random.uniform(-initstate.Ravg, initstate.Ravg, size=2)

    daughter = Cell(
        id=-1,
        pos=daughter_pos,
        is_mother=False,
        parent_id=cell.id,
        founder_id=cell.founder_id if cell.founder_id is not None else cell.id,
        subcolony_id=cell.subcolony_id,
        colony_id= cell.id
    )

    init_cycle(daughter)

    if daughter.cycle_time > 0:
        daughter.CI = 1.0 / daughter.cycle_time
        
    lineage_ins = Lineage()

    lineage_ins.update_ids(daughter)
    
    cell.CP = 0.0
    
    cell.R = cell.R_max


    return daughter
    
        
     

