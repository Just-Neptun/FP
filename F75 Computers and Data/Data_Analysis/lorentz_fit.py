import numpy as np

FIT_PARAM_NAMES = ('f_0', 'omega_0', 'gamma')

def curve(f, f_0, omega_0, gamma):
    '''Lorentz Resonance Curve (fit) function'''
    omega = 2 * np.pi * f
    return f_0 / np.sqrt((omega_0**2 - omega**2)**2 + gamma**2 * omega**2)


def calc_Q_factor(params, params_err):
    '''Calculate quality factor Q and its error from Lorentz curve fit parameters'''
    omega_0 = params[1]
    gamma = params[2]
    omega_0_err = params_err[1]
    gamma_err = params_err[2]
    Q = omega_0 / gamma
    Q_err = Q * np.sqrt((omega_0 / omega_0_err)**2 + (gamma_err / gamma)**2)
    return Q, Q_err