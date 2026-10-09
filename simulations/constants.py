"""Physical constants (CODATA 2018 / IAU nominal values).

Every number here is a real constant; see the comment on each line.
"""

import math

G = 6.67430e-11          # m^3 kg^-1 s^-2
C = 299792458.0          # m s^-1
HBAR = 1.054571817e-34   # J s
K_B = 1.380649e-23       # J K^-1
L_P = 1.616255e-35       # m
M_P = 2.176434e-8        # kg
T_P = 5.391247e-44       # s
M_SUN = 1.98847e30       # kg  (IAU nominal)
M_MOON = 7.348e22        # kg
LN2 = math.log(2.0)
LN10 = math.log(10.0)


def schwarzschild_kretschmann(M, r):
    """Kretschmann scalar of the Schwarzschild geometry, R_abcd R^abcd."""
    return 48.0 * G ** 2 * M ** 2 / (C ** 4 * r ** 6)


def hawking_temperature(M):
    return HBAR * C ** 3 / (8.0 * math.pi * G * M * K_B)


def bekenstein_hawking_entropy(M):
    """S/k_B in nats."""
    r_s = 2.0 * G * M / C ** 2
    area = 4.0 * math.pi * r_s ** 2
    return area / (4.0 * L_P ** 2)


def evaporation_time(M):
    """Power-law lifetime t = M^3 * 5120 pi G^2 / (ħ c^4)."""
    return M ** 3 * 5120.0 * math.pi * G ** 2 / (HBAR * C ** 4)
