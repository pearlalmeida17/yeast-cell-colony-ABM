from dataclasses import dataclass
from src.config.base_config import simulparams
import numpy as np

Vectors = tuple [float, float]

@dataclass
class Cell:
    #___must be provided___
    def __init__(self, id, is_mother, pos, parent_id=None, founder_id =None, colony_id=0, subcolony_id=None, bud_site_angle=None, bud_scars=None, birth_time = 0.0):
        
        self.id =  id # type: ignore
        self.parent_id = parent_id
        self.founder_id = founder_id
        self.colony_id = colony_id
        self.subcolony_id = subcolony_id

        
        self.is_mother = is_mother
        self.pos = np.array(pos, dtype=float) # type: ignore
        self.vel = np.zeros(2)

        
        #Assign max radius with ±10% variation
        self.R_max = (1 + np.random.uniform(-0.1,0.1))* simulparams.R_avg
        self.R :float = 0.0 

         # cycle
        self.G1: float = 0.0
        self.G2: float = 0.0
        self.CP: float = 0.0
        self.CI: float = 0.0
        self.CI_original: float = 0.0
        self.cycle_time: float = 0.0


        #Cell Progree CP ∈ [0,1]
        self.CP = 0.0
        self.cycle_time = self.G1 + self.G2
        

        #bud-related 
        self.bud_scars = bud_scars if bud_scars is not None else []


        self.bud_site_angle = bud_site_angle

        self.has_bud = False
        self.bud = None
        self.bud_age = 0.0

        self.subdomain_idx : tuple[int, int] | None = None

        self.birth_time = float(birth_time)
        self.birth_pos = self.pos.copy()


    
    

    



