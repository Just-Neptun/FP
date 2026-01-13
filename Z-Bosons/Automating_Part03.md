# 6.3 Automating Things

## 2. `eventloop.py`

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

## 3.

Rapidity:
$$ y = \frac{1}{2} \ln \frac{E + p_z}{E - p_z} $$
For low ratio of jet mass / jet energy:
$$ p_z \approx E \cos \theta $$
For negligible jet mass, pseudorapidity:
$$ \eta = - \ln \Big( \tan \frac{\theta}{2} \Big) \\
\eta = y $$

Invariant mass of the two leading leptons:

$$ p_T^2 = p_x^2 + p_y^2 $$
