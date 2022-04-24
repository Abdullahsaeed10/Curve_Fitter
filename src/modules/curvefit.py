import numpy as np
from numpy import fft
from abc import ABC, abstractmethod

from modules.utility import print_debug


class Signal():
    """Represents a signal"""

    def __init__(self, signal=[], fsample=0, time=[]) -> None:

        self.signal = signal
        self.fsample = fsample

        if self.fsample == 0:
            self.time = time
            if len(time) != 0:
                self.fsample = time[-1]/len(self.signal)
        else:
            self.time = np.arange(0, len(signal)) / fsample

        if (self.signal != [] and self.time == []) or (self.signal == [] and self.time != []):
            raise Exception("Signal must have a time or fsampling vector")

    def __len__(self):
        if self.signal != []:
            return len(self.signal)
        else:
            print_debug("Signal has 0 length")
            return 0

    def __subtract__(self, other):
        """Subtracts two signals"""
        if self.fsample == other.fsample:
            return Signal(self.signal - other.signal, self.fsample, self.time)
        else:
            raise Exception("Signals must have the same sampling frequency")

    def set_max_samples(self, max_samples):
        """Sets the maximum number of samples"""
        if len(self.signal) > max_samples:
            self.signal = self.signal[:max_samples]
            self.time = self.time[:max_samples]

    def chunk(self, chunk_size):
        return [self.signal[i:i + chunk_size] for i in range(0, len(self.signal), chunk_size)]


class Interpolation(ABC):
    """Represents a curve interpolation method"""

    @abstractmethod
    def interpolate(self) -> Signal():
        """Interpolates the curve"""

    @abstractmethod
    def set_signal(self, signal: Signal()):
        """Sets the signal to be interpolated"""


class PolynomialInterpolation(Interpolation):
    """Represents a polynomial curve interpolation method"""

    def __init__(self, signal: Signal() = None, order: int = None):
        self.signal = signal
        self.order = order
        self.interpolated_signal = Signal()

    def set_signal(self, signal: np.ndarray):
        """Sets the signal to be interpolated"""
        self.signal = signal

    def interpolate(self):
        """Interpolates the curve"""

        if self.signal is None or self.order is None:
            raise Exception("Signal and order must be set")

        self.interpolated_signal = Signal(signal=np.polyval(np.polyfit(
            self.signal.time, self.signal.signal, self.order), self.signal.time), fsample=self.signal.fsample)

        self.interpolated_signal = Signal(np.zeros(len(self.signal)))


class SplineInterpolation(Interpolation):
    """Represents a spline curve interpolation method"""

    def __init__(self, signal: np.ndarray = None, order: int = None, chunk_size=None, chunk_overlap=None):
        self.signal = signal
        self.order = order
        self.interpolated_signal = np.zeros(len(signal))

    def interpolate(self):
        """Interpolates the curve"""
        return self.interpolated_signal


class SignalProcessor():
    def __init__(self, original=Signal()) -> None:
        self.original_signal = original
        self.interpolation = None
        self.extrapolation = None
        pass

    def set_interpolation(self, interpolation: Interpolation = PolynomialInterpolation()):
        self.interpolation = interpolation
        self.interpolation.set_signal(self.original_signal)
        self.interpolation.interpolate()

    def extrapolate(self):
        pass

    def clip_signal(self, percentage):
        # extrapolates remaining samples
        pass

    def calculate_error(self):
        # progress bar

        # multithreading
        # https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
        pass


def update_graph(self):
    self.curve_plot.plot(self.signal.time, self.signal.signal)
    pass


def update_error_graph(self):

    pass
