from src.config.base_config import simulparams

from src.core.simulation import run_simulation

def run( **kwargs):
    return run_simulation(**kwargs)

