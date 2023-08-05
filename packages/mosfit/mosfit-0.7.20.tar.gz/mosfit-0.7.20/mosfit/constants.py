"""List of numerical constants, faster than using astropy with every call."""

import astropy.constants as c
import astropy.units as u
import numpy as np

LIKELIHOOD_FLOOR = -np.inf
LOCAL_LIKELIHOOD_FLOOR = -1.0e8

IPI = 1.0 / np.pi

ANG_CGS = u.Angstrom.cgs.scale
AU_CGS = u.au.cgs.scale
C_CGS = c.c.cgs.value
DAY_CGS = u.day.cgs.scale
FOE = 1.0e51
FOUR_PI = 4.0 * np.pi
KM_CGS = u.km.cgs.scale
M_SUN_CGS = c.M_sun.cgs.value
MAG_FAC = 2.5
MPC_CGS = u.Mpc.cgs.scale
