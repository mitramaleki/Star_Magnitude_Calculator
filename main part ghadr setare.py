from astropy.io import fits
import numpy as np
from photutils.aperture import CircularAperture, CircularAnnulus
from photutils import aperture_photometry
#This code is written by Mitra Maleki
def calculate_magnitude(ref_mag, ref_flux, star_flux):
    magnitude = ref_mag - 2.5 * np.log10(star_flux / ref_flux)
    return magnitude

def find_optimal_flux(image_data, x, y, max_aperture_radius=14, step_size=0.5):
    y, x = int(round(y)), int(round(x))
    reference_flux = image_data[y, x]

    # Adjust max_aperture_radius based on star position
    if y == 624 and x == 1263:  # Adjust these coordinates based on the position of the nebula star
        max_aperture_radius = 5
    else:
        max_aperture_radius = 14

    # Initialize variables for the best aperture and its flux
    best_aperture = None
    best_flux = 0.0
    best_snr = 0.0

    # Ratio for inner and outer radii
    ratio = 2.4  # You can adjust this value based on your preference

    # Try different aperture sizes and find the one with the highest SNR
    for current_aperture_radius in np.arange(0.5, max_aperture_radius + step_size, step_size):
        aperture = CircularAperture((x, y), r=current_aperture_radius)
        phot_table = aperture_photometry(image_data, aperture)
        flux = phot_table['aperture_sum'][0]

        # Calculate the noise and SNR for the current aperture
        gain = 1.0  # Define the gain value
        readnoise = 1.0  # Define the read noise value
        n_pixels = np.pi * current_aperture_radius ** 2
        noise = np.sqrt(flux * gain + n_pixels * readnoise ** 2)
        snr = flux * gain / noise

        # Calculate the inner and outer radii and the sky background flux
        inner_radius = current_aperture_radius * 12.5
        outer_radius = current_aperture_radius * 15.5
        sky_aperture = CircularAnnulus((x, y), r_in=inner_radius, r_out=outer_radius)
        sky_table = aperture_photometry(image_data, sky_aperture)
        sky_flux = sky_table['aperture_sum'][0]
        sky_area = np.pi * (outer_radius ** 2 - inner_radius ** 2)
        sky_background_flux = sky_flux / sky_area

        # Subtract the sky background flux from the star flux to get the total flux
        total_flux = flux - sky_background_flux * n_pixels

        # Update the best aperture if the current SNR is higher
        if snr > best_snr:
            best_snr = snr
            best_flux = total_flux
            best_aperture = aperture

    return best_flux, best_aperture

def main():
    # Load the FITS image
    fits_path = r"C:\Users\mitra\Desktop\python ghadr\stars.fits"
    hdul = fits.open(fits_path)
    image_data = hdul[0].data

    # Define reference star position and magnitude
    ref_x, ref_y = 425.01049660550996, 786.8934083356211
    reference_mag = 8.88

    # Find the optimal flux for the reference star
    reference_flux, _ = find_optimal_flux(image_data, ref_x, ref_y)

    # Define the positions of the stars in the lower frame
    stars_positions = [(715.8165450282543, 1401.7292606360122), (679.021905582712, 1474.8332234119366), (638.9827770887206, 1564.5375855023449)]

    # Define gain and readnoise
    gain = 1.0
    readnoise = 1.0

    # Calculate and print the magnitude, error, SNR, and flux for each star in the lower frame
    print("Magnitudes, Errors, Signal-to-Noise Ratios, and Fluxes for stars in the lower frame:")
    for x, y in stars_positions:
        star_flux, aperture = find_optimal_flux(image_data, x, y)
        magnitude = calculate_magnitude(reference_mag, reference_flux, star_flux)

        # Calculate the error and SNR for the current star
        inner_radius = aperture.r * 12.5
        outer_radius = aperture.r * 15.5
        sky_aperture = CircularAnnulus((x, y), r_in=inner_radius, r_out=outer_radius)
        sky_table = aperture_photometry(image_data, sky_aperture)
        sky_flux = sky_table['aperture_sum'][0]
        sky_area = np.pi * (outer_radius ** 2 - inner_radius ** 2)
        sky_background_flux = sky_flux / sky_area
        star_area = np.pi * aperture.r ** 2
        star_background_flux = sky_background_flux * star_area
        total_flux = star_flux - star_background_flux
        snr = total_flux / np.sqrt(total_flux * gain + star_area * readnoise ** 2)
        error = 1.08 / snr
        flux_per_pixel = sky_background_flux
        star_flux = total_flux / star_area
        print(f"Star at position ({x}, {y}): Magnitude = {magnitude:.2f}, Error = {error:.5f}, SNR = {snr:.2f}, Flux = {star_flux:.2f}")

    # Define the position of the faint star near the planet-like nebula
    faint_star_x, faint_star_y = 1262.9954386931731, 624.3259890929296

    # Calculate and print the magnitude, error, SNR, and flux for the faint star
    faint_star_flux, aperture = find_optimal_flux(image_data, faint_star_x, faint_star_y)
    faint_star_magnitude = calculate_magnitude(reference_mag, reference_flux, faint_star_flux)
    inner_radius = aperture.r * 12.5
    outer_radius = aperture.r * 15.5
    sky_aperture = CircularAnnulus((faint_star_x, faint_star_y), r_in=inner_radius, r_out=outer_radius)
    sky_table = aperture_photometry(image_data, sky_aperture)
    sky_flux = sky_table['aperture_sum'][0]
    sky_area = np.pi * (outer_radius ** 2 - inner_radius ** 2)
    sky_background_flux = sky_flux / sky_area
    star_area = np.pi * aperture.r ** 2
    star_background_flux = sky_background_flux * star_area
    total_flux = faint_star_flux - star_background_flux
    snr = total_flux / np.sqrt(total_flux * gain + star_area * readnoise ** 2)
    error = 1.08 / snr
    faint_star_flux_per_pixel = sky_background_flux
    faint_star_flux = total_flux / star_area
    print(f"Faint star near the planet-like nebula at position ({faint_star_x}, {faint_star_y}): "
          f"Magnitude = {faint_star_magnitude:.2f}, Error = {error:.5f}, SNR = {snr:.2f}, Flux = {faint_star_flux:.2f}")

    hdul.close()

if __name__ == "__main__":
    main()
