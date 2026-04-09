# Adjusting Weights

- `projs` and `pops` are projection and population collectors, respectively.
- `run()` takes a population and gives back a spike collector and the membrane potential
- `plot_data()` takes a population collector, a spike collector, and a membrane potential and plots them over time, i.e. there are two subplots.
    - The first subplot is a plot of the pair (time of spike, neuron id) for each spiked neuron.
    - The second subplot is the membrane trace of the first excited neuron.

There are five weights: `stim_exc`, `stim_inh` `exc_exc`, `exc_inh`, `inh_exc`.
The allowed values are integers from 0-63 (negative in the last case).
