# Introduction

Simple package to help with calculation of aerosol optical properties and derived parameters.
The code uses the [miepython](https://github.com/scottprahl/miepython) implementation of the
Wiscombe code developed by Scott Prahl for the Mie calculations.

#### Lognormal
The equation describing the distribution is:

```math
\frac{dn}{dr} = \frac{n}{\sqrt{2\pi}r\ln\sigma_g}\exp\left(-\frac{(\ln(r)-\ln(r_g))^2}{2\ln^2\sigma_g}\right)
```

where $`r_g`$ is median radius, and $`\sigma_g`$ is the width.

## Installation

Clone the repository and then

```
pip install -e .
```

## Example Usage
```
from aerosol_optprop.lognormal import AerosolLognormal

# create a lognormal distribution and compute the cross section
aerosol = AerosolLognormal(median_radius=0.1, width=1.5)
aerosol.cross_section(wavelength=0.525)

# update the particle number density using a fixed extinction
print(aerosol.n)
aerosol.set_n_from_extinction(extinction=1e-3, wavelength=0.525, persistant=True)
print(aerosol.n)

# calculate derived parameters
aerosol.surface_area_density
aerosol.mode_radius = 0.1  # set the mode radius of the distribution
aerosol.median_radius  # median radius has been automatically updated
aerosol.extinction(wavelength=0.525)  # extinction is unchanged
aerosol.n  # number density has been updated
```