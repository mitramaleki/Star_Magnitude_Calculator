
# FITS Image Star Photometry Tool

## Overview

This tool performs aperture photometry on stars in a FITS image to calculate their magnitudes, errors, signal-to-noise ratios (SNR), and fluxes. It finds the optimal flux for each star and uses a reference star to calculate magnitudes.

## Features

- Reads FITS images.
- Performs aperture photometry to find optimal flux.
- Calculates magnitudes, errors, SNRs, and fluxes for specified stars.
- Adjusts aperture size for stars near nebulae.

## Dependencies

- `astropy`: For handling FITS images.
- `numpy`: For numerical operations.
- `photutils`: For aperture photometry.

You can install these dependencies using the following command:

```sh
pip install astropy numpy photutils
```

## Usage

1. Clone the repository:

```sh
git clone https://github.com/yourusername/fits-star-photometry-tool.git
cd fits-star-photometry-tool
```

2. Update the `fits_path` variable in the `main` function to point to your FITS image file:

```python
fits_path = r"C:\Users\mitra\Desktop\python ghadr\stars.fits"
```

3. Run the script:

```sh
python main.py
```

## Example Output

```
Magnitudes, Errors, Signal-to-Noise Ratios, and Fluxes for stars in the lower frame:
Star at position (715.8165450282543, 1401.7292606360122): Magnitude = 9.32, Error = 0.01234, SNR = 25.78, Flux = 1234.56
Star at position (679.021905582712, 1474.8332234119366): Magnitude = 10.15, Error = 0.01567, SNR = 20.45, Flux = 987.65
Star at position (638.9827770887206, 1564.5375855023449): Magnitude = 8.78, Error = 0.01023, SNR = 30.12, Flux = 2345.67

Faint star near the planet-like nebula at position (1262.9954386931731, 624.3259890929296): Magnitude = 12.34, Error = 0.02345, SNR = 15.67, Flux = 456.78
```

## How It Works

### Calculating Magnitudes

The `calculate_magnitude` function calculates the magnitude of a star given its flux, using a reference star's magnitude and flux.

### Finding Optimal Flux

The `find_optimal_flux` function performs aperture photometry on a star to find the optimal flux and SNR by trying different aperture sizes.

### Main Function

The `main` function:
1. Loads the FITS image.
2. Defines the reference star's position and magnitude.
3. Finds the optimal flux for the reference star.
4. Defines positions of stars in the lower frame and calculates their magnitudes, errors, SNRs, and fluxes.
5. Calculates the same parameters for a faint star near a planet-like nebula.
