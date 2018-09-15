import numpy as np


def read_lta_file(filename):
    """ Read wavemeter data from an lta file

    Parameters
    ----------
    filename : str
        Filename of lta file

    Returns
    -------
    np.ndarray
        2d numpy array. 1st col: time in ms, 2nd col: wavelength in nm
    """
    skip_lines = 0
    with open(filename) as f:
        for line in f:  # Skip header
            if not line.startswith('Time  [ms]'):
                skip_lines += 1
            else:
                break
    data = np.loadtxt(filename, skiprows=skip_lines + 1)
    return data
