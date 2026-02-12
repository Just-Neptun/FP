# 6.5 Comparing Data and MC

## 1. Merging Data

- We use the `hadd` utility to merge the electron and muon data files.

## 2. Plotting the Comparison

- We modify the provided script `plot.py` to produce a figure where the combined data (black) and the contributions of the MC electrons (blue), muons (green), and taus (red)
- We need to scale the MC calculations to $1\,\mathrm{fb}^{-1}$.

![Comparison of Data and MC Calculations of Z Mass](Plots_pngs/5_2-comparison.png)

- The distribution of the merged data matches the combined distributions from the MC simulation.
- We note that the tau distribution is not in the same position, but its contribution to the MC distribution is small/negligible. Therefore, the graphs still match very well.

The tau distribution because:
___________