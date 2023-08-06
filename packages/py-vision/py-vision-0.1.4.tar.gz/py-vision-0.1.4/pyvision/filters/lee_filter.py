from scipy.ndimage.filters import uniform_filter

def lee_filter(band, window, var_noise = 0.25):
    """
    Expects single band from SAR image, already re-shaped

    :param band: single band data from SAR image
    :param window: descpeckling filter window
    :param var_noise: noise variance, default = 0.25

    """
    
    mean_window = uniform_filter(band, window)
    mean_sqr_window = uniform_filter(band**2, window)
    var_window = mean_sqr_window - mean_window**2

    weights = var_window / (var_window + var_noise)
    band_filtered = mean_window + weights*(band - mean_window)

    return band_filtered