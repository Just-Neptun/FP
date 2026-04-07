# Preparation

## Overview

- Neurons
- Neuromorphic computing
- Silicon neurons (Lu.i)
- BrainScaleS-2
    - feedforward network
    - sudoku solver

## Theory

- Neurons consist of the soma (core), dendrites (input), and the axon (output)
- Synapses connect presynaptic axon to postsynaptic dendrites
- Neurotransmitters can carry an input signal
- This excites or inhibits the membrane potential
- This might spike the membrane potential, causing it to send signals to other neurons

- negative resting potential
- postsynaptic potential $\epsilon_{ij}(t)$
- spike if exceeding critical threshold, causing hyperpolarization
- if not exceeding, PSP-stacking

- Leaky integrate-and-fire model
- ignore different spike shapes
- model needs to include a spiking mechanism
- Model: Membrane = capacitor, leakage = resistance, resting potential = source, stimulation = current
- spike has to be modelled through a different circuit

- Adaptive exponential model
- Adaptation current, exponential threshold

- Synaptic plasticity
- Weight corresponds to how a signal gets transmitted to the postsynaptic neuron
- phenomenological models describe input/output relationship
