import random, math
from cell import Cell
from config import cellcycle

def choose_bud_site(cell):
    if  not cell.bud_scars:
        angle = random.uniform(0, 2 * math.pi)
    else:
        scar = random.choice(cell.bud_scars)
        option = random.choice(['opposite', 'adjacent'])
        direction = random.choice(['clockwise', 'anticlockwise'])
        
        
        if option == 'opposite':
            angle = scar + math.pi
        else:
            if direction == 'clockwise':
                angle = scar - math.radians(10) 
            else:
                angle = scar +  math.radians(10)
    
    return angle

def spawn_bud( cell,  new_id: int):
    angle = choose_bud_site(cell)
    bud_x = cell.pos[0] + cell.radius * math.cos(angle)
    bud_y = cell.pos[1] + cell.radius * math.sin(angle)

    return Cell(
        id=new_id, 
        pos=(bud_x, bud_y), 
        radius=0.5,
        mother_id=cell.id,
        doubling_time=random.gauss(cellcycle.total_daughter, cellcycle.total_daughter_sd),
        subcolony_id=cell.subcolony_id,
        is_bud=True)

def detach_bud(mother, bud):
    bud.is_bud = False
    bud.age = 0
    bud.doubling_time = max(random.gauss(cellcycle.total_mother, cellcycle.total_mother_sd), 30)
    bud.base_doubling_time = bud.doubling_time  # ← keep base in sync too!
    mother.bud_id = -1
    dx= bud.pos[0] - mother.pos[0]
    dy = bud.pos[1] - mother.pos[1]

    angle = math.atan2(dy, dx)
    mother.bud_scars.append(angle)