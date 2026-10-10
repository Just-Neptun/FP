import numpy as np
import matplotlib.pyplot as plt
from sympy import Q

free_freqs = np.array([137.127, 859.362, 2407.239])
measured_freqs = np.array([125, 825, 2298])

c = np.array([-0.327, 0.108, 0.524])


def calc_resonance_freq(n, Q):
    return free_freqs[n] * np.sqrt(1 + c[n] / Q**2)


def get_res_freqs(Q):
    return np.array([calc_resonance_freq(n, Q) for n in range(3)])


Q_mid = 39664310
Q_range = np.arange(39_600_000, 39_700_000, 1)
resonance_range = get_res_freqs(Q_range).T
print(f"For Q = 1: {get_res_freqs(1)}")
print(resonance_range[:5, :])
print((resonance_range - measured_freqs)[:5, :])
std_range = np.sum((resonance_range - measured_freqs) ** 2, axis=1)
print(Q_range[np.argmin(std_range)], get_res_freqs(Q_range[np.argmin(std_range)]))


# Q range 1 to 100
# for each Q: calculate resonance freqs
# subtract the measured and square
# sum the three squared vals
# find the minimum over all Qs
