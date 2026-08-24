from cell import Cell
from config import initstate, cellcycle
from cell_cycle import grow, is_ready_to_divide
from budding import spawn_bud, detach_bud
from integrator import step_positions
from nutrients import nutrient_factor
import random


class Colony:
    def __init__(self, budding : bool, nutrient_limited: bool):
        self.cells = []
        self.time = 0
        self.next_id = 1  
        self.next_subcolony_id = 1
        self.budding = budding
        self.nutrient_limited = nutrient_limited

        founder =  Cell(
            id= 0 ,
            pos = (0, 0),
            radius = 2.58 ,
            doubling_time = max(random.gauss(cellcycle.total_mother, cellcycle.total_mother_sd), 30) ,
            subcolony_id = 0,

        )
        self.cells.append(founder)

    def step (self, dt):

        for cell in self.cells:
            grow(cell, dt)

        for cell in self.cells:
            
            if is_ready_to_divide(cell) and cell.bud_id == -1:
                
                if self.budding:
                    new_bud = spawn_bud(cell, self.next_id)
                    cell.bud_id = new_bud.id
                    cell.age = 0
                    if cell.id == 0:
                        new_bud.subcolony_id = self.next_subcolony_id
                        self.next_subcolony_id += 1
                    
                    self.cells.append(new_bud)
                    self.next_id +=1
                
                else:
                    pass
        centers = [cell.pos for cell in self.cells]
        new_centers = step_positions(centers, self.cells)
        for cell, new_pos in zip(self.cells, new_centers):
            cell.pos = new_pos

        for cell in self.cells:
            if cell.is_bud and cell.radius >= initstate.Ravg:
                mother = next(c for c in self.cells if c.id == cell.mother_id)
                detach_bud(mother, cell)

        for cell in self.cells:
            factor = nutrient_factor(cell, self.cells, self.nutrient_limited)
            if factor > 0:
                cell.doubling_time = cell.base_doubling_time / factor
        
        self.time += dt

