from math import pi
import electron

class Force:
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        raise NotImplementedError

##########################
### PHYSICAL CONSTANTS ###
##########################

E_MASS   = 9.11E-31 # kg
E_CHARGE = 1.60E-16 # C

LIGHT_SPEED = 3.0E8 # m / s

VACUUM_PERMITTIVITY = 8.85E-12    # C^2 / (N * m^2)
VACUUM_PERMEABILITY = pi * 4.0E-7 # (T * m) / A

COULOMBS_LAW_CONSTANT = 9.0E9 # (N * m^2) / C^2


######################
### GAME CONSTANTS ###
######################

ELECTRON_MAGNETIC_FIELD_SCALE = 2e-3
ELECTRON_CHARGE = -16

MAX_MAGNETIC_FIELD = 0.3 # T

SUBSTEPS = 64