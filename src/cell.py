from dataclasses import dataclass, field
from typing import List, Tuple

Vectors = tuple [float, float]

@dataclass
class Cell:
    #___must be provided___

    id: int
    pos: Vectors
    radius: float
    doubling_time: float
    subcolony_id: int

    #___default___

    age: float = 0.0
    mother_id: int =-1
    bud_id: int = -1
    is_bud: bool = False
    bud_scars: List[float] = field(default_factory=list)
    base_doubling_time : float = 0.0
    birth_radius: float = 0.0

    def __post_init__(self):
        self.base_doubling_time = self.doubling_time
        self.birth_radius = self.radius
