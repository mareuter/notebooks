import numpy as np

__all__ = ["ephem_magnitude"]


def ephem_magnitude(elongation, earth_distance_au):
	BASE_MAGNITUDE = -12.7
	CONST_TERM = np.log(np.pi)
	TERM1 = np.log(np.pi / 2.0 * (1 + 1e-6 - np.cos(elongation)))
	TERM2 = np.log(earth_distance_au / 0.0025)
	mag = BASE_MAGNITUDE + 2.5 * (CONST_TERM - TERM1) + 5 * TERM2
	return np.floor(mag * 100.0 + 0.5) / 100.0