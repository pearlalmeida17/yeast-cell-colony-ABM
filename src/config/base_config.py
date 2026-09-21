from __future__ import annotations
from dataclasses import dataclass
from typing import Final
import math

@dataclass (frozen = True)
class PhysicalConstants:
    Kb: Final[float] = 1.380649e-23 # Boltzmann constant in J/K
    T: Final [float] = 300.00 # Temperature in Kelvin (26.85°C)

@dataclass(frozen = True)
class ModelParams:
    Kb = PhysicalConstants.Kb
    T = PhysicalConstants.T

    #physical parameters
    sigma: Final [float] = 0.3 #incompressibility of the yeast cell
    E: Final [float]  = 1000  #Young's modulus in kPa (Mechanical properties of yeast cell wall)
    phi: Final [float] = 1e15 #density of surface adhesion molecules in cell area (m^-2)
    Ws: Final [float]= 25 *Kb * T  # Single Bond binding energy
    Kbud: Final [float] = 25  #Attachment of new bud to mother cell
    eta: Final [float] = 2.5  #Viscosity of growth medium 

@dataclass (frozen = True)
class cellcycle:
    #cell cycle
    G2avg: float = 75 #avg length of G2 phase in mins
    G1avgdaughter: float = 45 #avg length of G1 phase in mins (new daughter)
    G1avgmother: float = 15 #avg length of G1 phase in mins (mother cell)
    total_daughter: float = 120  # total cycle = G1 + G2
    total_mother: float = 90     # total cycle = G1 + G2
    total_mother_sd : float = 9.0
    total_daughter_sd :float = 12.

@dataclass (frozen = True)
class simulparams:
    #simulation parameters
    total_time: float = 1440 #total simulation time in mins for now to begin with 10 time steps
    dt: float = 0.00144 #time step in mins
    R_avg: float = 2.58
    r : float = 0.003 #Rate of Maximum Cell Cycle Adjustment, Controls the amount cell cycle is adjusted at each time step

@dataclass
class initstate:
    #inital state of the 3 cells. 
    # Assuming the radii of the cells are in microns
    #Radii of the three cells
    cell_radii = {
        0 : 2.2, #radius of cell 1 in microns   
        1 : 2.4, #radius of cell 2 in microns
        2 : 2.1  #radius of cell 3 in microns
    }


    cell_centers = {
    #cell centers for 3 cells
        0 :(0.0, 0.0),
        1 :(4.2, 0.0),
        2 :(1.5, 2.0)
    }

#cell geometry    
    Ravg: float = 2.58 #avg radius of yeast cell in microns
    Mjmax: float = 18*math.pi* Ravg**2 #max possible biomass for each subdomain
    di_t: float = 25 #subdomain size, area of each subdomain in microns^2

#Nutrient condition
    NUTRIENT_LIMITED = True

#Budding condition
    BUDDING = True
        