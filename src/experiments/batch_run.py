from ..simulation.engine import run
from config.base_config import initstate

def batch_run(n_runs=5, budding=True, nutrient=True):
    initstate.BUDDING = budding
    initstate.NUTRIENT_LIMITED = nutrient

    results = []
    for k in range(n_runs):
        cells, lineage = run()
        results.append((cells, lineage))
        print(f"Run {k+1}: N = {len(cells)}")
    return results
