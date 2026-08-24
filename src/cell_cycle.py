from config import initstate, simulparams

def grow(cell, dt):
    growth_rate = (initstate.Ravg - cell.birth_radius)/cell.base_doubling_time

    increased_radius = growth_rate * (simulparams.dt)

    cell.radius = min(cell.radius + increased_radius, initstate.Ravg)
    cell.age += dt

    
def is_ready_to_divide(cell):
    return cell.age >= cell.doubling_time
