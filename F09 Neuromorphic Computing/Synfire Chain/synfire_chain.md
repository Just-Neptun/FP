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

In the upper subplot, we see the pair (time of spike, neuron id) for each spiked neuron.
There are two regions, the excitatory populations show up in the lower (red) region, while the inhibitory populations show up in the upper (blue) region.
In our case, there are eight clusters each, each representing a population.
This implies that each population only has one simultaneous spike and then returns to their resting potential, which is exactly the behaviour of a synfire chain.
The lower subplot shows further how fast the inhibitory populations counteract the spiking behaviour of the excitatory populations.

## Which connection affects the synfire chain behavior the most?

The connection responsible for the characteristic behaviour of a synfire chain is `inh_exc`.
Of course all others are also necessary, but this connection makes it such that each population has the explicit function of exciting the next population before it gets killed off.
This is what distinguishes the synfire chain from a network of repeatedly spiking populations, in which no structure is present.

## What happens if you disable inhibition?

We test this by setting `stim_inh` and `exc_inh` to zero.

As predicted in the last answer, each excitatory population keeps spiking until it runs out of fuel.
Meanwhile, it repeatedly excites the following population, which therefore can keep spiking for longer.
This process compounds, until the last population spikes approximately 25 times.
Needless to say, this would not benefit a human brain.

## Visualize the membrane potential of the neuron using the oscilloscope.

- Turns out we cloned the wrong branch
- Save image task1 from osc and plot

# Adjusting the number of neurons

## Which hardware feature limits the minimal number of neurons in each population?

## What is the maximal chain length that you can produce?
