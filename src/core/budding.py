import random, math
from cycle import init_cycle
from core.cell import Cell
from config.base_config import initstate
from lineage import lineage
import numpy as np



def choose_bud_site_angle(cell):
    # No Budding scar yet; only 1 scar from the mother; hence, a daughter cell's first bud
    if  len(cell.bud_scars) == 1:
        angle = (cell.bud_scars[-1] + math.pi ) % (2 * math.pi)
    else:    
        if random.random() < 0.5:
            angle = (cell.bud_scars[-1] + math.pi ) % (2 * math.pi)
        else:
            angle_offset = math.radians(random.uniform(-10, 10))
            angle = (cell.bud_scars[-1] + angle_offset) % (2 * math.pi)
        
        
    if angle in cell.bud_scars:
        choose_bud_site_angle(cell)
    else:
        #set the angle to the cell until the bud is attached to it 
        cell.bud_site_angle = angle
        #angle is in radians
        return angle
    


def maybe_start_bud(cell):
    if not initstate.BUDDING:
        return
    if cell.in_G2() and not cell.has_bud:
        cell.has_bud = True
        cell.bud_age = 0.0

        if not cell.bud_site_angle:
            cell.bud_site_angle = choose_bud_site_angle(cell)

        cell.bud = {
            "R" : 0.0,
            "angle" : cell.bud_site_angle,
            "pos": cell.pos.copy()

        }


def create_daughter_from_bud(cell):
    daughter = Cell(
        id = None,
        is_mother = False,
        pos = cell.bud["pos"],
        R_avg = initstate.Ravg,
        G1_avg_mother=cell.G1,
        G1_avg_daughter=cell.G1,
        G2_avg=cell.G2,
        parent_id=cell.id,
        founder_id=cell.founder_id if cell.founder_id is not None else cell.id,
        colony_id=cell.colony_id,
        
    )
    
    init_cycle(daughter)
    lineage.update_ids(daughter)

    #what happens to cell.bud_site_angle after creation of daughter cell
    cell.bud_site_angle = None
    cell.bud_scars.append(cell.bud["angle"])
    cell.CP = 0.0
    return daughter


#bud_growth rate() and bud_attach_time() implementation? -- add  

def update_bud( cell,dt,):
    if not initstate.BUDDING or not cell.has_bud:
        return None

    bud_attach_time = cell.G2
    bud_growth_rate = initstate.Ravg/ bud_attach_time

    cell.bud_age += dt
    cell.bud["R"] += bud_growth_rate * dt

    if not cell.bud_site_angle:
        maybe_start_bud(cell)

    ux = np.cos(cell.bud["angle"])
    uy = np.sin(cell.bud["angle"])
    direction = np.array([ux,uy])

    cell.bud["pos"] = cell.pos + (cell.R + cell.bud["R"]) * direction

    if cell.bud_age >= bud_attach_time:
        cell.has_bud = False
        return create_daughter_from_bud(cell)

    return None

def handle_non_budding_divison(cell):
    if initstate.BUDDING:
        return None
    if cell.CP >= 1.0:
        daughter_pos = cell.pos + np.random.uniform(-initstate.Ravg, initstate.Ravg, size=2)
        daughter = Cell(
            id=-1,
            pos=daughter_pos,
            is_mother=False,
            parent_id=cell.id,
            founder_id=cell.founder_id if cell.founder_id is not None else cell.id,
            colony_id= cell.id
        )
    
        init_cycle(daughter)
        lineage.update_ids(daughter)

        cell.CP = 0.0
        return daughter
    return None
        
     

