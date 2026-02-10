# 6.2 Getting to Know the Basics

## 2. The `vxp_z` variable

Plotting `vxp_z`:

![vxp_z graph](Plots_pngs/Part02/2_2.png)

`vxp_z` is a float data type \
it is the z-position of the primary vertex in mm \
z-position is along the path of the particles, z axis along the beam pipe
center of the collider is at $z=0$

The graph shows number of measurements / entries at each position. It is a histogram with number of entries vs position of collision in millimeters. \
We can read off the average position of the vertex (mean), as well as the standard deviation of the distribution.

Why this (mostly Gauss) distribution? \
Random variable is normally distributed. \
Aim is to have collision at $z=0$, different sources of random error combine to cause Gauss distribution of position. \
Also CLT.

## 3. Describe data

LHC Bunches are about 30 cm long, taking about 1 ns to travel their length. \
They make up a beam of particles. It is easier to concentrate particles more closely when theuy are in bunches rather than a uniform beam. \
They are spaced by 25 ns. 2808 bunches out of 3564 can contain protons.

Really there are two peaks very close to each other.

### Questions:
What are LHC bunches, and how are they related to the vxp_z plot in question 2? How many peaks do you see in the vxp_z distribution? Explain possible reasons. What type of plot could help you answering this question? Hint: Maybe you can even find it under https: // twiki. cern. ch/ twiki/ bin/ view/ AtlasPublic/ BeamSpotPublicResults .

## 4. `lep_n` variable

Plotting `lep_n`:

![lep_n graph](Plots_pngs/Part02/2_4.png)

`lep_n` = Number of preselected leptons

Shown is how many leptons were detected for the relevant event. \
This is the number of counted leptons in the final state.

## 5. Describe data

We expect 1, 2 or 3 leptons in the final state, depending on the specific decay process.
In leading order we expect 2 leptons.
The other numbers correspond to non-leading-order processes.
Also, neutrinos are not detected, allowing odd numbers of leptons.

Feynman diagrams of the 1, 2, 3 lepton processes go here!

## 6. `lep_pt`, `lep_eta` and `lep_phi`

Plotting `lep_pt`, `lep_eta` and `lep_phi`:

![lep_pt graph](Plots_pngs/Part03/3_2-lep_pt.png)
![lep_eta graph](Plots_pngs/Part03/3_2-lep_eta.png)
![lep_eta log scale graph](Plots_pngs/Part03/3_2-lep_eta-log.png)
![lep_phi graph](Plots_pngs/Part03/3_2-lep_phi.png)

`lep_pt` is the Transverse momentum of the lepton (transverse to what!?) \
`lep_eta` is the Pseudorapidity of the lepton \
`lep_phi` is the Azimuthal angle of the lepton

For graphing `lep_pt` and `lep_eta`, these are saved as vectors (conceptually `list`s like in `python`) because multiple leptons can be detected in one collision. Each one has its own momentum and pseudorapitity which are single components of the `lep_pt` and `lep_eta` vectors.

The histograms consolidate all of these measurements, so they can have more total entries/measurements than there were collisions.

### Many Questions

