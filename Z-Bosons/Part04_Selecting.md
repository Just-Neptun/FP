# 6.4 Selecting Events

## 1. Cut Flow Histogram

## 2. Applied Cuts

We apply a series of cuts to our data and create a cut-flow histogram to show how much data is being removed/kept at each step.

#### Isolation cut:

We want events *without* other particles around our collision products. This means we should cut out events which have other energy/momentum in the same region of the detector where the lepton passed through.

This cuts out events where the lepton might have interacted with other particles and *lost energy to surroundings*, because that would not be accounted for in our calculation.

We create a histogram of $p_{Tcone}/p_T$ to see its distribution and to select a reasonable cutoff.

We restrict `Etcone20 / E` and `ptcone30 / pt` to $\leq x$ 

#### $M_Z$ cut:

We restrict the invariant mass to a reasonable range:

$$ x \leq M_Z \leq x $$