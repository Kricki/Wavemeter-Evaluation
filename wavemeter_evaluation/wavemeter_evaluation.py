import numpy as np
import math

from . import wavemeter_data as wmd


def find_nearest(array, value):
    """ Find the nearest value in array.

    The array must be sorted.

    From https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array

    Parameters
    ----------
    array : numpy.ndarray
        array to be searched
    value : float
        value to be found

    Returns
    -------
    int, float
        Index and value of nearest match in array

    """
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1, array[idx-1]
    else:
        return idx, array[idx]


class WavemeterEvaluation:
    def __init__(self):
        """"
        data_time : numpy.ndarray
            Array containing the time data (in seconds)
        data_wavelength : numpy.ndarray:
            Array containing the wavelength data (in nm)
        data_frequency : numpy.ndarray
            Array containing the frequency data (in GHz)
        n_files : int
            Number of loaded files
        """
        self._data_time = np.empty(0)
        self._data_wavelength = np.empty(0)
        self._data_frequency = np.empty(0)

        self._n_files = 0

    @property
    def data_time(self):
        return self._data_time

    @property
    def data_wavelength(self):
        return self._data_wavelength

    @property
    def data_frequency(self):
        return self._data_frequency

    @property
    def n_files(self):
        return self._n_files

    def add_data_from_file(self, filename, encoding='utf-8'):
        """ Add data from an lta-file.

        Data will be added to the attributes data_time, data_wavelength, data_frequency.
        The time will be appended to existing data.

        Parameters
        ----------
        filename : str
            Filename of the data file to be added
        encoding : str
            Encoding of the data file, defaults to 'utf-8'

        """
        data = wmd.read_lta_file(filename=filename, encoding=encoding)

        data = np.delete(data, (np.where(data[:, 1] < 0)), 0)  # remove negative values (correspond to under- or overexposure)

        data_time = data[:, 0]/1000  # time in seconds
        data_wavelength = data[:, 1]  # wavelength in nm
        data_frequency = 299792458/data_wavelength  # frequency in GHz

        if np.shape(self._data_time)[0] > 0:
            # there is already data => append new data to existing data
            # offset the time to match the end of the existing data
            time_offset = self._data_time[-1]
            data_time += time_offset

        self._data_time = np.append(self._data_time, data_time)
        self._data_wavelength = np.append(self._data_wavelength, data_wavelength)
        self._data_frequency = np.append(self._data_frequency, data_frequency)

        self._n_files += 1

    def clear_data(self):
        """ Clears the data.

        """
        self._data_time = np.empty(0)
        self._data_wavelength = np.empty(0)
        self._data_frequency = np.empty(0)
        self._n_files = 0

    def info(self):
        """ Prints information about current object.

        """
        if self._n_files > 0:
            print('Number of loaded files: ' + str(self._n_files))
            print('Total measurement time: ' + str(self._data_time[-1]) + ' s')
        else:
            print('No files loaded.')

    def calculate_statistics(self, mode='frequency', print_output=False):
        """ Calculates statistic of the data:

        Mean, Standard deviation, Minimum value, Maximum value, Difference between miniimum and maximum value

        Parameters
        ----------
        mode : str
            Identifier to choose the data to process. Can be "wavelength" or "frequency".
        print_output : bool
            If True, result will be printed to the console. Defaults to False.

        Returns
        -------
        list
            List with the statistcs results.
            [mean, standard deviation, minimum value, maximum value, difference between min and max]
        """
        if mode == 'frequency':
            data = np.copy(self._data_frequency)
            text = 'Frequency statistics:'
            unit = 'GHz'
        elif mode == 'wavelength':
            data = np.copy(self._data_wavelength)
            text = 'Wavelength statistics:'
            unit = 'nm'
        else:
            raise(ValueError('Invalid parameter for "mode"'))

        mean = np.mean(data)
        stddev = np.std(data)
        min_value = np.amin(data)
        max_value = np.amax(data)
        diff_minmax = np.abs(max_value-min_value)

        if print_output:
            print(text)
            print('--------------------------------')
            print('Mean: ' + str(mean) + ' ' + unit)
            print('Standard deviation: ' + str(stddev) + ' ' + unit)
            print('Minimum value: ' + str(min_value) + ' ' + unit)
            print('Maximum value: ' + str(max_value) + ' ' + unit)
            print('Delta(max, min): ' + str(diff_minmax) + ' ' + unit)
            print('--------------------------------')

        return [mean, stddev, min_value, max_value, diff_minmax]

    def calculate_stability(self, time_delta, mode='frequency'):
        """ Calculate stability of the measured wavelength

        Returns an array containing the differences between measurement values (wavelength of frequency) at a temporal
        distance time_delta.

        Parameters
        ----------
        time_delta : float
            Difference between measurement values
        mode : str
            Identifier to choose the data to process. Can be "wavelength" or "frequency".
        Returns
        -------
        numpy.ndarray
            Array containing the differences between measurement values

        """
        if mode == 'frequency':
            data = np.copy(self._data_frequency)
        elif mode == 'wavelength':
            data = np.copy(self._data_wavelength)
        else:
            raise(ValueError('Invalid parameter for "mode"'))

        diff = []
        for time, val in zip(self._data_time, data):
            idx, _ = find_nearest(self._data_time, time+time_delta)
            diff.append(val-data[idx])

        return np.array(diff)
