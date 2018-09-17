import numpy as np


def read_lta_file(filename, encoding='utf-8'):
    """ Read wavemeter data from an lta file

    Parameters
    ----------
    filename : str
        Filename of lta file
    encoding : str
        Encoding of the data file, defaults to 'utf-8'

    Returns
    -------
    np.ndarray
        2d numpy array. 1st col: time in ms, 2nd col: wavelength in nm
    """

    ##  Determine how long the header is
    skip_lines = 0
    with open(filename, encoding=encoding) as f:
        for line in f:
            if not line.startswith('[Measurement data]'):
                skip_lines += 1
            else:
                break

    ## Read data from file
    data = np.genfromtxt(filename, skip_header=skip_lines + 3, delimiter='\t', encoding=encoding)
    data = data[:, [0,1]]  # only keep the first two colummns (time and wavelength of channel 1)
    data = data[~np.isnan(data).any(axis=1)]  # remove all rows containing NaNs

    return data
