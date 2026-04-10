# Adjusting Weights

- `projs` and `pops` are projection and population collectors, respectively.
- `run()` takes a population and gives back a spike collector and the membrane potential
- `plot_data()` takes a population collector, a spike collector, and a membrane potential and plots them over time, i.e. there are two subplots.
    - The first subplot is a plot of the pair (time of spike, neuron id) for each spiked neuron.
    - The second subplot is the membrane trace of the first excited neuron.

There are five weights: `stim_exc`, `stim_inh` `exc_exc`, `exc_inh`, `inh_exc`.
The allowed values are integers from 0-63 (negative in the last case).

## Tune weights to achieve behaviour of synfire chain

- Start by setting `stim_exc = 63` and `stim_inh = 31` to observe how the populations evolve without interaction [img].
  We see that `exc` has two spikes before returning to its resting potential, while `inh` only has one.
- Including `inh_exc = -31` counteracts the second peak of `exc`. [img]
  This is the desired behaviour of a single population.
- Finally, including `exc_exc = 63` and `exc_inh = 31` mimics the initial stimulation and thus lets the following populations show the same behaviour.

## Explain how the visualized plot relates to the synfire chain behavior.

## Which connection affects the synfire chain behavior the most?

## What happens if you disable inhibition?

## Visualize the membrane potential of the neuron using the oscilloscope.
