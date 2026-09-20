from core.colony import Colony
from config.base_config import simulparams

from ..core.simulation import run_simulation

def run():
    cells, lineage = run_simulation()
    # hook into analysis/visualization if you want
    return cells, lineage

