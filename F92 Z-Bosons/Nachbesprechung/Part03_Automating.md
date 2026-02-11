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

MC simulation to find what we would expect from the data.
(Simulated distribution matches quite well to measured distribution.)

![Invariant Mass graph](Plots_pngs/Part03/3_5-initial.png)

TODO:
How do you expect the distribution to look like for the decay of a Z boson – and why might it not look like your expectation when running over the DataEgamma.root file? How many peaks can you identify, and what do they belong to? Hint: Try single and/or double logarithmic axis scales. Now run your analysis over the Monte Carlo file mc_147770.Zee.root and compare the results for the invariant mass distribution.