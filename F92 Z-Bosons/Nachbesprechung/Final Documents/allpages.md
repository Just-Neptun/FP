# 6.2 Getting to Know the Basics

## 2. The `vxp_z` variable

#### Plotting `vxp_z`:

![vxp_z graph](Plots_pngs/Part02/2_2.png)

`vxp_z` is a float data type \
it is the z-position of the primary vertex in mm \
z-position is along the path of the particles, z axis along the beam pipe \
center of the collider/collision is at $z=0$

The graph shows number of measurements / entries at each position. It is a histogram with number of entries vs position of collision in millimeters. \
We can read off the average position of the vertex (mean), as well as the standard deviation of the distribution.

#### Why this (mostly Gauss) distribution?
Random variable is normally distributed. \
Aim is to have collision at $z=0$, different sources of random error combine to cause Gauss distribution of position. \
Also Central Limit Theorem (CLT) means the sum of many random variables follows a distribution approaching a Gaussian.

## 3. Describe data

LHC Bunches are about 30 cm long, taking about 1 ns to travel their length. \
They make up a beam of particles. It is easier to concentrate particles more closely when they are in bunches rather than a uniform beam. \
They are spaced by 25 ns. For each beam 2808 bunches out of 3564 can contain protons.

Every filled bunch slot contains typically $N_i = O(10^{11})$ protons.

We see the distribution of the collision of two bunches.

Really there are two peaks very close to each other in the `vxp_z` graph. This could be because of the collision center moving between fills.

From website, we can see that for the 2012 run the collision center moved over time. Maybe this caused the two peaks.

![Beam Spot Position Graph from Website](Analysis_Images/Part02/beamspot-2012-plot-posZ.png)

Additionally, the distribution of protons inside a bunch is relevant.
A plot of this would be helpful.
If their distribution has two humps, so might the vertex position. 

## 4. `lep_n` variable

#### Plotting `lep_n`:

![lep_n graph](Plots_pngs/Part02/2_4.png)

`lep_n` = Number of preselected leptons

The graph shows how many leptons were detected for the measurement/event. \
This is the number of counted leptons in the final state.

## 5. Describe data

In this part, we are talking only about how many leptons we actually *detected* in the final state. Therefore, neutrinos are ignored.

We expect 2 leptons in the final state.
1, 2 or 3 leptons in the final state are also possible, depending on the specific decay process. \
In leading order we expect 2 leptons.
The other numbers correspond to non-leading-order processes.
Also, neutrinos are not detected, allowing odd numbers of leptons.

Feynman diagrams of the 1, 2, 3 lepton processes go here!

The dominant process for 1-lep final:
$$ \bar u + d \overset{W^-}{\longrightarrow} e^- + \bar \nu_{e} $$

The dominant process for 2-lep final (q is any quark):
$$ \bar q + q \overset{Z^0}{\longrightarrow} e^- + e^+ $$

The dominant process for 3-lep final (combine previous 2):
$$ \bar u + d \longrightarrow e^- + \bar \nu_{e} + e^+ + e^- $$

## 6. `lep_pt`, `lep_eta` and `lep_phi`

Plotting `lep_pt`, `lep_eta` and `lep_phi`:

![lep_pt graph](Plots_pngs/Part03/3_2-lep_pt.png)

`lep_pt` is the Transverse momentum of the lepton (transverse to the beam direction)

The cutoff happens because an event must contain at least one lepton with $p_T > 25$ GeV. Otherwise, it is not recorded. This is a systematic cut off/*trigger* (not triggering means the event is not recorded/it is cut from the data).

The second cutoff is for events with two or more leptons, (at least one with $p_T > 25$ GeV). The other momenta measurements are not considered leptons if $p_T > 5$ GeV. An event like this is considered a 1 lepton event.

![lep_eta graph](Plots_pngs/Part03/3_2-lep_eta.png)
![lep_eta log scale graph](Plots_pngs/Part03/3_2-lep_eta-log.png)

`lep_eta` is the Pseudorapidity of the lepton

Leptons are distributed uniformly in pseudorapidity. The gaps/cutoffs are because of detector geometry.

![lep_phi graph](Plots_pngs/Part03/3_2-lep_phi.png)

`lep_phi` is the Azimuthal angle of the lepton

Leptons are again distributed uniformly in azimuthal angle.

---

For graphing `lep_pt` and `lep_eta`, these are saved as vectors (conceptually `list`s like in `python`) because multiple leptons can be detected in one collision. Each one has its own momentum and pseudorapidity which are single components of the `lep_pt` and `lep_eta` vectors.

The histograms consolidate all of these measurements, so they can have more total entries/measurements than there were collisions.

# 6.3 Automating Things

## 2. `eventloop.py`

#### What the script does:

In order:

- catch input errors
- open given file
- load ROOT tree
- make new `.root` file to save to later
- make a new histogram object with `ROOT.TH1D(...)`
- loop over all collisions:
    - in each, read out all data for the collision (check for success)
    - fill `vxp_z` for that collision into the histogram object
- write all histograms inside the new `.root` file
- by default, create a popup window/canvas with the created histogram
    - wait for user input before the popup is closed

We limited to 100,000 entries.

![vxp_z graph](Plots_pngs/Part03/3_2-vxp_z.png)

![lep_n graph](Plots_pngs/Part03/3_2-lep_n.png)

Converted MeV to GeV in below graph:

![lep_pt graph](Plots_pngs/Part03/3_2-lep_pt.png)

![lep_eta graph](Plots_pngs/Part03/3_2-lep_eta.png)

## 3. Invariant Mass

Rapidity:
$$ y = \frac{1}{2} \ln (\frac{E + p_z}{E - p_z}) $$
By trigonometry:
$$ p_z = |\vec{p}| \cdot \cos (\theta)  $$
For low ratio of jet mass / jet energy (highly relativistic particles):
$$ E \approx p $$
$$ y \approx \frac{1}{2} \ln (\frac{p + p_z}{p - p_z}) $$
$$ y \approx \frac{1}{2} \ln (\frac{p + p \cdot \cos (\theta)}{p - p \cdot \cos (\theta)}) $$
$$ y \approx \frac{1}{2} \ln (\frac{1 + \cos (\theta)}{1 - \cos (\theta)}) $$
$$ y \approx \frac{1}{2} \ln (\frac{2 \cos^2 (\frac{\theta}{2})}{2 \sin^2 (\frac{\theta}{2})}) $$
$$ y \approx \frac{1}{2} \ln (\tan^{-2} (\frac{\theta}{2})) $$

This gives us the pseudorapidity:
$$ \eta = - \ln \Big( \tan \frac{\theta}{2} \Big) \\
\eta \approx y $$

Invariant mass of the two leading leptons:

$$ m_0^2 c^2 = \frac{E^2}{c^2} - \vec{p}^2 $$

---
Measured values: $E, p_T, \eta$, but we want to calculate mass, which needs $p_z$ as well.

---

$$ p_z = p_T \cdot \cot (\theta) $$
$$ p_z = p_T \cdot \frac{\cos (\theta)}{\sin (\theta)} $$
$$ p_z = p_T \cdot \frac{\cos^2 (\frac{\theta}{2}) - \sin^2 (\frac{\theta}{2})}{2 \sin (\frac{\theta}{2}) \cos (\frac{\theta}{2})} $$
$$ p_z = p_T \cdot \frac{\cot (\frac{\theta}{2}) - \tan (\frac{\theta}{2})}{2} $$
$$ p_z = p_T \cdot \frac{e^\eta - e^{-\eta}}{2} $$
$$ p_z = p_T \cdot \sinh (\eta) $$
Then:
$$ p_T^2 = p_x^2 + p_y^2 \\
p^2 = p_T^2 + p_z^2 \\
p^2 = p_T^2 \cdot (1 + \sinh^2 (\eta)) $$

Now substitute into the equation for invariant mass:

$$ m_0^2 = \frac{E^2}{c^4} - \frac{\vec{p}^2}{c^2} \\
m_0^2 = \frac{E^2}{c^4} - p_T^2 \cdot (1 + \sinh^2 (\eta)) / c^2 $$

We apply the equation to variables and graph histogram of result. We restrict/disallow negative $m_0^2$ so that all masses are positive.

![Invariant Mass graph](Plots_pngs/Part03/3_3-inv_mass.png)

## 4. `TLorentzVector`

![Invariant Mass graph](Plots_pngs/Part03/3_4.png)

Both methods do the same thing and produce very similar histograms.

## 5. Expected Distribution

A priori, one might expect a symmetric distribution around the expected value of ~$90\,\mathrm{GeV}$.
For example, a Gaussian or Breit-Wigner distribution.

This generally true, but we can also see smaller peaks at around ~$3\,\mathrm{GeV}$ and ~$9.5\,\mathrm{GeV}$.
These coincide with the rest masses of the $\mathrm{J}/\Psi$ and $\Upsilon$ mesons.
These can decay into a $\gamma^*$, which can then become two leptons (meaning the event is included in the data, even after filtering).

We also see a "hill" due to the $25\,\mathrm{GeV}$ cutoff.

MC simulation to find what we would expect from the data.
(Simulated distribution matches quite well to measured distribution.)

![Invariant Mass graph](Plots_pngs/Part03/3_5-initial.png)

# 6.4 Selecting Events

## 1. Cut Flow Histogram

We apply a series of cuts to our data and create a cut-flow histogram to show how much data is being removed/kept at each step.

![Cut Flow Histogram](Plots_pngs/Part04/4-2-cutflow-real.png)

List of cuts:
- Weights: MC weighting
- Trigger: Check `trigE` or `trigM` is true (electron or muon trigger from dataset)
- GRL: Good run list, checks if event is marked as a good run (Data Quality Group assessment)
- Vertex: Check `hasGoodVertex` variable, meaning primary vertex/position of collision is well determined.
- >= 2 Leptons: Check that at least two leptons were detected (otherwise it is not a Z decay event)
- PDGID (Particle Data Group Identifiers): check `lep_type` variable and make sure the measured particles are leptons ($e, \mu, \tau$).
- Charge: Z Boson is neutral so the decay products must have opposite charges.
- $p_T$ Cut: leptons must have at least $25$ GeV of transverse momentum (leptons are expected to split their momenta to half of the Z mass), cutoff below this.
- Isolation Cut ($p_T$): see below
- Isolation Cut ($E$): see below
- Tight ID: We want to have data with harsher identification criteria
- Z Mass Cut: see below

The most effective cut is the cut requiring at least two leptons be produced and measured in the event. \
Next most effective is the $p_T$ cut.

### Isolation cut:

We want events *without* other particles around our collision products. This means we should cut out events which have other energy/momentum in the same region of the detector where the lepton passed through.

This cuts out events where the lepton might have interacted with other particles and *lost energy to surroundings*, because that would not be accounted for in our calculation.

We create a histogram of $p_{Tcone}/p_T$ to see its distribution and to select a reasonable cutoff.

![pt Cone Ratio](Plots_pngs/Part04/4_2-isolation-pt.png)

We restrict `Etcone20 / E` and `ptcone30 / pt` to $\leq 0.13$ as our cutoff limits.

### $M_Z$ cut:

We restrict the invariant mass to a reasonable range:

$$ 60 \ \mathrm{GeV}/c^2 \leq M_Z \leq 120 \ \mathrm{GeV}/c^2 $$


## 3. Applying to Datasets

We run the cutting process on all the events on the following files, creating invariant mass histograms for all of them.

- `DataEgamma.root`
- `DataMuons.root`
- `mc_147770.Zee.root`
- `mc_147771.Zmumu.root`
- `mc_147772.Ztautu.root`

---

![DataEgamma Graph of Invariant Mass](Plots_pngs/Part04/4_3-DataEgamma.png)

![DataMuons Graph of Invariant Mass](Plots_pngs/Part04/4_3-DataMuons.png)

![MC Electrons Graph of Invariant Mass](Plots_pngs/Part04/4_3-MCZee.png)

![MC Muons Graph of Invariant Mass](Plots_pngs/Part04/4_3-MCZmumu.png)

![MC Tauons Graph of Invariant Mass](Plots_pngs/Part04/4_3-MCZtautau-revised.png)

The last graph clearly does not show have a peak at the expected ~$90$ GeV. This is because the tauons produced in a Z decay can themselves decay very quickly in many ways:

$$ \tau^- \overset{W^-}\longrightarrow \ell^- + \bar \nu_\ell + \nu_\tau $$
$$ \tau^- \overset{W^-}\longrightarrow \text{hadrons} + \nu_\tau $$

And for anti-tauons:

$$ \tau^+ \overset{W^+}\longrightarrow \ell^+ + \nu_\ell + \bar \nu_\tau $$
$$ \tau^+ \overset{W^+}\longrightarrow \text{hadrons} + \nu_\tau $$

(about 17% per lepton branch, 65% decay into hadrons)

Firstly, we are only looking at lepton decays. Filtering out the most likely decay means we are losing a lot of tauon events.

For the decays where Z bosons become $\tau^\pm$, these can decay again into the above leptons. Because neutrinos are not detected, we do not measure the total energy/mass/momentum. Without the neutrinos, the reconstructed Z candidate has too low mass.

# 6.5 Comparing Data and MC

## 1. Merging Data

- We use the `hadd` utility to merge the electron and muon data files.

## 2. Plotting the Comparison

- We modify the provided script `plot.py` to produce a figure where the combined data (black) and the contributions of the MC electrons (blue), muons (green), and taus (red)
- We need to scale the MC calculations to $1\,\mathrm{fb}^{-1}$.
```python
xsec_e = 8175.7172
sumw_e = 203795455568148
xsec_m = 9953.0232
sumw_m = 225316022111048
xsec_t = 1346.6041
sumw_t = 31508540303680.9
lumi   = 1000
```
$$ \text{Scale Factor} = \frac{\text{Luminosity} \times \text{Cross-Section}}{\text{Sum of Weights}} $$

![Comparison of Data and MC Calculations of Z Mass](Plots_pngs/5_2-comparison.png)

- The distribution of the merged data matches the combined distributions from the MC simulation.
- We note that the tau distribution is not in the same position, but its contribution to the MC distribution is small/negligible. Therefore, the graphs still match very well.

# 6.6 Fitting the Z Mass

## 1. Plotting the Fit Functions

![Various Fit Functions on Invariant Mass Graph](Plots_pngs/6_2-fitfunctions.png)

The Breit-Wigner curve is the true distribution of the mass according to QM/SR (see $\Gamma$ explanation below).

For a real measurement (with some finite detector resolution), we also have statistical non-QM errors, which cause a Gaussian distribution (CLT).

The measured mass comes from:
$$ m_{measured} = m_{true, \ BW} + \epsilon_{error, \ G} $$

General convolution for probability:
$$ X = Y + Z $$
$$ f_X(x) = \int f_Y(y) \cdot f_Z(x - y) \ \mathrm{d}y $$

## 2. Extracting Fit Parameters

Due to mass-energy-momentum relativistic relation and finite lifetimes $\tau$, the uncertainty relation $\Delta x \ \Delta p >= \frac{\hbar}{2}$ can be written like $\Delta t \ \Delta E >= \frac{\hbar}{2}$ relates uncertainty in time with uncertainty in invariant mass.
$$ \Gamma = \frac{\hbar}{\tau} $$

Using the best fitting model (convolution): \
Invariant Mass:
$$ M_Z = (90.556 \pm 0.005) \ \mathrm{GeV} $$
Decay width (see above):
$$ \Gamma = (3.826 \pm 0.014) \ \mathrm{GeV} $$
Uncertainty/Standard Deviation:
$$ \sigma = (1.471 \pm 0.010) \ \mathrm{GeV} $$

---

Particle Data Group:
$$ M_Z = (91.1880 \pm 0.0020) \ \mathrm{GeV} $$
$$ \Gamma = (2.4955 \pm 0.0023) \ \mathrm{GeV} $$

---

$\sigma$-Deviations:
$$ M_Z \text{ Deviation: } 120 \ \sigma $$
$$ \Gamma \text{ Deviation: } 94 \ \sigma $$
Including the standard deviation for the $M_Z$ error:
$$ M_Z \text{ Deviation: } 0.43 \ \sigma $$
# 6.7 Determining Efficiencies

Efficiency is how well we detect particles as the correct ones (e.g. electrons).

Tag and probe: strict selection criteria on the tagged electron, the second one becomes the probe, which is used to determine efficiency.

- tag and probe method
- tag has to pass selection criteria
- probe has to be checked (is it an electron?)
- efficiency is fraction of probes passing

$$ \epsilon_{total} = \epsilon_{reconstruction} \times \epsilon_{identification} \times \epsilon_{trigger} \times \epsilon_{additional} $$
# 6.8 Systematic Errors

## Evaluating Possible Sources of Error

beginning with the calculation on event level up to the fitting of the invariant di-lepton mass distribution – you should be able to identify a variety of error candidates.
