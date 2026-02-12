import numpy as np

def abweichung(a, a_error, b, b_error=0.0) -> float:
    return np.abs(a - b) / np.sqrt(a_error**2 + b_error**2)

M_Z   = 90.556
Gamma =  3.826
M_Z_error   = 0.005
Gamma_error = 0.014

M_Z_theo   = 91.1880
Gamma_theo =  2.4955
M_Z_theo_error   = 0.0020
Gamma_theo_error = 0.0023

print(abweichung(M_Z, M_Z_error, M_Z_theo, M_Z_theo_error))
print(abweichung(Gamma, Gamma_error, Gamma_theo, Gamma_theo_error))
