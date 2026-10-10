import numpy as np
import pandas as pd

def vertical_line(ax, position: float, height=10.0, label="", color="tab:grey"):
    '''Plots a vertical line at `position` on axes `ax`.'''
    axes = ax.axis()
    ax.vlines(position, -height, height, label=label, colors=color, linestyles="--")
    ax.axis(axes)

def pd_freq_spectrum(fig, axs, data: pd.DataFrame):
    X = data["A"] * np.cos(data["phi"])
    Y = data["A"] * np.sin(data["phi"])

    ax1, ax2, ax3 = axs[0], axs[1], axs[2]
    ax1.errorbar(data["freq"], data["A"], yerr=data["A_err"])
    ax1.set_xlabel(r"$\nu$ / Hz")
    ax1.set_ylabel(r"$A$ / Vpp")
    ax1.set_title("Resonance Curve (Amplitude)")
    
    ax2.errorbar(data["freq"], data["phi"], yerr=data["phi_err"])
    ax2.set_xlabel(r"$\nu$ / Hz")
    ax2.set_ylabel(r"$\phi$")
    ax2.set_title("Phase Shift")

    ax3.errorbar(data["freq"], X, label="$X = A \\cos (\\phi)$")
    ax3.errorbar(data["freq"], Y, label="$Y = A \\sin (\\phi)$")
    ax3.set_xlabel(r"$\nu$ / Hz")
    ax3.set_ylabel(r"Amplitude / Vpp")
    ax3.set_title("Waveform Chart")
    ax3.legend()

    return fig, axs