import numpy as np

from scipy.optimize import curve_fit

FIT_PARAM_NAMES = ('f_0', 'omega_0', 'gamma')

def curve(f, f_0, omega_0, gamma):
    '''Lorentz Resonance Curve (fit) function'''
    omega = 2 * np.pi * f
    return f_0 / np.sqrt((omega_0**2 - omega**2)**2 + gamma**2 * omega**2)

def fit_analysis(ax, freq, A, A_err, p0):
    '''Fit Lorentz curve to given data and plot on given axes `ax`'''
    params, pcov = curve_fit(
        curve,
        freq,
        A,
        p0=p0,
        sigma=A_err,
        absolute_sigma=True
    )
    params_err = np.sqrt(np.diag(pcov))

    xgrid = np.linspace(np.min(freq), np.max(freq), 300)
    ax.plot(xgrid, curve(xgrid, *params), label="Fit Curve")
    
    return params, params_err

def calc_Q_factor(params, params_err):
    '''Calculate quality factor Q and its error from Lorentz curve fit parameters'''
    omega_0 = params[1]
    gamma = params[2]
    omega_0_err = params_err[1]
    gamma_err = params_err[2]
    Q = omega_0 / gamma
    Q_err = Q * np.sqrt((omega_0 / omega_0_err)**2 + (gamma_err / gamma)**2)
    return Q, Q_err

def do_fit(ax, freq, A, A_err, p0=(0.002, 1, 1)):
    result_dict = {}

    params, params_err = fit_analysis(ax, freq, A, A_err, p0)
    for param_name, param, param_err in zip(FIT_PARAM_NAMES, params, params_err):
        result_dict[param_name] = param
        result_dict[param_name + '_err'] = param_err

    Q, Q_err = calc_Q_factor(params, params_err)

    result_dict['fit_Q_factor'] = Q
    result_dict['fit_Q_err'] = Q_err
    result_dict['params_list'] = params
    result_dict['params_err_list'] = params_err

    return result_dict