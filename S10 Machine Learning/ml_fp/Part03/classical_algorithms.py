import numpy as np
import matplotlib.pyplot as plt
import time

from typing import Literal

from matplotlib.colors import ListedColormap

from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SUBFIG_WIDTH = 3
SUBFIG_HEIGHT = 3

def example_of_algorithms(
        classifiers,
        classifiers_names,
        datasets,
        datasets_names,
    ):
    '''
    Create a figure with subfigures: (x=classifiers+empty, y=datasets).
    During this, record runtimes and accuracy score to return as list of dicts.
    '''
    results = []

    figure = plt.figure(figsize=(
        SUBFIG_WIDTH * len(classifiers),
        SUBFIG_HEIGHT * len(datasets)
    ))
    i = 1
    # iterate over datasets
    for ds_cnt, (ds, ds_name) in enumerate(zip(datasets, datasets_names)):
        # print(f'Using ds_cnt: {ds_cnt}, ds: {ds}, ds_name: {ds_name}')
        # preprocess dataset, split into training and test part
        X, y = ds
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.4,
            random_state=42,
        )
        x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
        y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5

        # just plot the dataset first
        cm = plt.get_cmap('RdBu')
        cm_bright = ListedColormap(["#FF0000", "#0000FF"])
        ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
        if ds_cnt == 0:
            ax.set_title("Input data")

        ax.set_ylabel(ds_name)
        # Plot the training points
        ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors="k")
        # Plot the testing points
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6, edgecolors="k")
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_xticks(())
        ax.set_yticks(())
        i += 1

        # iterate over classifiers
        for clf_cnt, (name, clf) in enumerate(zip(classifiers_names, classifiers)):
            ax = plt.subplot(len(datasets), len(classifiers) + 1, i)

            clf = make_pipeline(StandardScaler(), clf)
            tr_st = time.perf_counter()
            clf.fit(X_train, y_train)
            tr_et = time.perf_counter()
            te_st = time.perf_counter()
            score = clf.score(X_test, y_test)
            te_et = time.perf_counter()
            DecisionBoundaryDisplay.from_estimator(
                clf, X, cmap=cm, alpha=0.8, ax=ax, eps=0.5
            )

            tr_rt = tr_et - tr_st
            te_rt = te_et - te_st
            results.append({
                'classifier': name,
                'dataset': ds_name, 
                'score': score,
                'train_runtime': tr_rt,
                'test_runtime': te_rt
            })

            # Plot the training points
            ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors="k")
            # Plot the testing points
            ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, edgecolors="k", alpha=0.6)

            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            ax.set_xticks(())
            ax.set_yticks(())
            if ds_cnt == 0:
                ax.set_title(name)
            ax.text(
                x_max - 0.3,
                y_min + 0.3,
                ("%.2f" % score).lstrip("0"),
                size=15,
                horizontalalignment="right",
            )
            i += 1

    plt.tight_layout()
    plt.show()

    return results


LEVEL_TO_BOOL = {
    "high": True,
    "low": False,
}

# create a desaturated cmap
cmap = plt.get_cmap("RdYlGn")
colors = cmap(np.linspace(0, 1, 256))
desat_factor = 0.8   # 0 = grayscale, 1 = original
gray = np.mean(colors[:, :3], axis=1, keepdims=True)
colors[:, :3] = gray + desat_factor * (colors[:, :3] - gray)
desat_cmap = ListedColormap(colors)

def style_dataframe(
        df,
        labels_to_style: list[str],
        good_sides: list[Literal["high", "low"]]
    ):
    '''
    Return a pandas style object which colors backgrounds of chosen columns (labels_to_style) with a gradient.
    green = good    ;    red = bad
    Pick the good/green values in good_sides from "high" or "low".
    '''

    styling_list = list(zip(labels_to_style, good_sides))

    # filter out columns which would be all NaNs
    # these will not be styled
    styling_list = [
        (label, good_side)
        for label, good_side in styling_list
        if df[label].notna().all()
    ]
    styled = df.style

    for label, good_side in styling_list:
        high_is_green = LEVEL_TO_BOOL[good_side]
        if high_is_green:
            styled.background_gradient(subset=[label], cmap=desat_cmap)    # low is red, high is green
        else:
            styled.background_gradient(subset=[label], cmap=desat_cmap.reversed())    # low is green, high is red

    return styled
