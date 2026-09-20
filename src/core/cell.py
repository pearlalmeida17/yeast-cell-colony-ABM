from dataclasses import dataclass
import numpy as np

Vectors = tuple [float, float]

@dataclass
class Cell:
    #___must be provided___
    def __init__(self, id_, is_mother, pos, R_avg, parent_id=None, founder_id =None, colony_id=0, subcolony_id=None, bud_site_angle=None, bud_scars=None):
        
        self.id: id_ # type: ignore
        self.parent_id = parent_id
        self.founder_id = founder_id
        self.colony_id = colony_id
        self.subcolony_id = subcolony_id

        
        self.is_mother = is_mother
        self.pos: np.array(pos, dtype=float) # type: ignore
        self.vel = np.zeros(2)

        
        #Assign max radius with ±10% variation
        self.R_max = (1 + np.random.uniform(-0.1,0.1))* R_avg
        self.R :float = 0.0 

         # cycle
        G1: float = 0.0
        G2: float = 0.0
        CP: float = 0.0
        CI: float = 0.0
        CI_original: float = 0.0
        cycle_time: float = 0.0

        

        #Cell Progree CP ∈ [0,1]
        self.CP = 0.0
        self.cycle_time = self.G1 + self.G2
        self.CI = 1.0 / self.cycle_time

        #bud-related 
        self.bud_scars = bud_scars if bud_scars is not None else []


        self.bud_site_angle = bud_site_angle

        self.has_bud = False
        self.bud = None
        self.bud_age = 0.0

        subdomain_idx: tuple[int, int] | None = None


    
    

    



