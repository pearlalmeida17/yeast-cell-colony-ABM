from colony import Colony
from config import simulparams




def run_simulation(budding, nutrient_limited):
    
    colony = Colony(budding, nutrient_limited)
    time_history = []
    cell_count_history = []

    while colony.time < 1440 and  len(colony.cells) < 15000:
        colony.step(simulparams.dt)
        time_history.append(colony.time)
        cell_count_history.append(len(colony.cells))

    return colony, time_history, cell_count_history

