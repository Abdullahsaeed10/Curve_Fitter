from importlib_metadata import NullFinder
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
        """Returns the length of the signal"""
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

    def clip(self, direction, percentage):
        """Clips the signal"""
        if direction == "left":
            self.signal = self.signal[int(
                len(self.signal) * (1 - percentage)):]
            self.time = self.time[int(len(self.time) * (1 - percentage)):]
        elif direction == "right":
            self.signal = self.signal[:int(
                len(self.signal) * (1 - percentage))]
            self.time = self.time[:int(len(self.time) * (1 - percentage))]
        else:
            raise Exception("Direction must be left or right")

    def chunk(self, chunk_size):
        return [self.signal[i:i + chunk_size] for i in range(0, len(self.signal), chunk_size)]


class Process(ABC):
    """Represents a generic process"""

    @abstractmethod
    def set_signal(self, signal: Signal()):
        """Sets the signal to be interpolated"""

    @abstractmethod
    def get_signal(self):
        """Returns the processed signal object"""


class Interpolation(Process):
    """Represents a curve interpolation interface"""

    @abstractmethod
    def interpolate(self) -> Signal():
        """Interpolates the curve"""


class PolynomialInterpolation(Interpolation):
    """Represents a polynomial curve interpolation method"""

    def __init__(self, signal: Signal() = None, order: int = None):
        self.signal = signal
        self.order = order
        self.interpolated_signal = Signal()

    def set_signal(self, signal: np.ndarray):
        """Sets the signal to be interpolated"""
        self.signal = signal
        self.interpolate()

    def get_signal(self):
        """Returns the interpolated signal object"""
        return self.interpolated_signal

    def interpolate(self):
        """Interpolates the curve"""

        if self.signal is None or self.order is None:
            raise Exception("Signal and order must be set")

        self.interpolated_signal = Signal(signal=np.polyval(np.polyfit(
            self.signal.time, self.signal.signal, self.order), self.signal.time), fsample=self.signal.fsample)


class SplineInterpolation(Interpolation):
    """Represents a spline curve interpolation method"""

    def __init__(self, signal: np.ndarray = None, order: int = None, chunk_size=None, chunk_overlap=None):
        self.signal = signal
        self.order = order
        self.interpolated_signal = np.zeros(len(signal)) 

    def interpolate(self):
        """Interpolates the curve"""
        return self.interpolated_signal


class Extrapolation(Process):
    """Represents an extrapolation interface"""

    @abstractmethod
    def extrapolate(self):
        """Extrapolates the curve"""
    @abstractmethod
    def set_output_range(self, range_start: int, range_end: int):
        """Sets the range of the output signal"""


class LinearPredictiveCoding(Extrapolation):
    """Represents a linear predictive coding extrapolation method"""

    def __init__(self, signal: Signal() = None, order: int = None):
        self.signal = signal
        self.extrapolated_signal = Signal()

    def set_signal(self, signal: Signal()):
        """Sets the signal to be extrapolated"""
        self.signal = signal
        self.extrapolate()


class SignalProcessor():
    def __init__(self, original=Signal()) -> None:
        self.original_signal = original
        self.output_signal = original
        self.interpolation = None
        self.extrapolation = None
        self.interpolated_signal = original
        self.extrapolated_signal = original
        pass

    def isInterpolated(self):
        if self.interpolation == None:
            return False
        else:
            return True

    def isExtrapolated(self):
        if self.extrapolation == None:
            return False
        else:
            return True

    def set_clipping(self, clip_percentage: int = 0):
        self.clip_percentage = clip_percentage

        if self.isExtrapolated():
            self.extrapolation.set_signal(
                self.original_signal.clip("right", self.clip_percentage))

    def set_interpolation(self, interpolation: Interpolation = PolynomialInterpolation()):
        self.interpolation = interpolation
        self.interpolation.set_signal(self.original_signal)

    def set_extrapolation(self, extrapolation: Extrapolation = LinearPredictiveCoding()):
        self.extrapolation = extrapolation
        self.extrapolation.set_signal(self.original_signal)

    def merge_output(self):
        pass

    def calculate_error(self):
        # progress bar

        # multithreading
        # https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
        pass


def update_graph(self):
    if self.signal_processor.isInterpolated():
        temp_signal = self.signal_processor.interpolation.get_signal()
        self.curve_plot_ref.setData(temp_signal.time, temp_signal.signal)
    else:
        self.curve_plot_ref.setData(
            self.signal_processor.original_signal.time, self.signal_processor.original_signal.signal)
    if self.signal_processor.isExtrapolated():
        self.curve_plot


def update_error_graph(self):

    pass
