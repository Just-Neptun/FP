import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def clf_analysis_plots(
    df: pd.DataFrame,
    target_accuracy,
    figsize,
    target_line_padding = 0.75,
    xticks_rotation = 25
    ):
    N_clf = len(df)

    fig, axes = plt.subplots(1, 2, figsize=figsize)
    ax1, ax2 = axes
    ax1.bar(df['name'], df['accuracy'])
    ax1.set_ylim(0.8, 1)
    ax1.hlines(
        target_accuracy,
        - target_line_padding,
        N_clf - 1 + target_line_padding,
        colors='tab:orange',
        label='Target Accuracy'
    )
    ax1.tick_params(axis='x', rotation=xticks_rotation)
    ax1.set_ylabel('Accuracy')
    ax1.legend()

    bar_pos = np.arange(N_clf)
    width = 0.8/2

    ax2.bar(bar_pos - width/2, df['training_runtime'], width, label='Training')
    ax2.bar(bar_pos + width/2, df['testing_runtime'], width, label='Testing')
    ax2.set_yscale('log')
    ax2.tick_params(axis='x', rotation=xticks_rotation)
    ax2.set_xticks(bar_pos)
    ax2.set_xticklabels(df['name'])
    ax2.set_ylabel('Runtime / s')
    ax2.legend()

    return fig, axes