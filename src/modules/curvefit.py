from importlib_metadata import NullFinder
import numpy as np
from numpy import fft
from abc import ABC, abstractmethod
from copy import copy

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

    def __getitem__(self, index):
        """Returns the signal at the given index"""
        return Signal(self.signal[index], self.fsample, self.time[index])

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
        percentage = percentage / 100
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

        self.chunk_count = len(self.chunks)


class SignalProcessor():
    def __init__(self, original=Signal()) -> None:

        self.original_signal = copy(original)

        self.clipped_signal = copy(original)
        self.clip_percentage = 100

        self.interpolation_type = None
        self.interpolation_order = None
        self.chunk_size = None

        self.extrapolation_type = None

        self.interpolated_signal = copy(original)
        self.extrapolated_signal = copy(original)

    def init_interpolation(self, type: str = None, order: int = 1, chunk_size: int = 0):
        if type == None:
            raise Exception("Interpolation type must be set")

        self.interpolation_type = type
        self.interpolation_order = order
        self.chunk_size = chunk_size
        self.interpolate()

    def interpolate(self):
        type = self.interpolation_type
        input = self.clipped_signal

        if type == "polynomial":
            self.interpolated_signal = Signal(signal=np.polyval(np.polyfit(
                input.time, input.signal, self.interpolation_order), input.time), fsample=input.fsample)

        if type == "spline":
            for chunk in input:
                """TODO: interpolate chunk by chunk and then add the overlap"""

    def extrapolate(self):
        
        """Extrapolates remaining signal, starting from N of clipped to N of original"""

        self.extrapolation_type = "linear predictive coding"

        N_clipped = len(self.clipped_signal)
        N_original = len(self.original_signal)

        """Processing Here"""
        #fitting the clipped signal

        self.coeff=np.polyfit(self.clipped_signal.time, self.clipped_signal.signal, self.interpolation_order)

        self.extrapolated_values=np.polyval(self.coeff,self.original_signal.time[N_clipped:N_original])

        """Output signal here"""
        self.extrapolated_signal=Signal(signal=self.extrapolated_values,time=self.original_signal.time[N_clipped:N_original])

        
       

    def set_clipping(self, clip_percentage: int = 0):
        if clip_percentage == 100:
            raise Exception("Clip percentage cant be 100%")

        self.clip_percentage = clip_percentage
        # Resets the clipped signal
        self.clipped_signal = copy(self.original_signal)
        self.clipped_signal.clip("right", self.clip_percentage)
        # interpolate
        # extrapolate
        # calculate error

    def overlap_add(self, chunk_size: int = 1, overlap_size: int = 1):
        # checks if last chunk
        # if not either then add overlap to the end of the next chunk
        pass

    def isInterpolated(self):
        if self.interpolation_type == None:
            return False
        else:
            return True

    def isExtrapolated(self):
        if self.extrapolation_type == None:
            return False
        else:
            return True

    def calculate_error(self, loading_counter: int = 0):
        # progress bar

        # multithreading
        # https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
        pass


def update_graph(self):
    if self.signal_processor.original_signal != None:
        draw = self.signal_processor.original_signal
        self.curve_plot_ref.setData(draw.time, draw.signal)

    if self.signal_processor.isInterpolated():
        draw = self.signal_processor.interpolated_signal
        self.curve_plot_interpolated.setData(draw.time, draw.signal)

    if self.signal_processor.isExtrapolated():
        draw = self.signal_processor.extrapolated_signal
        self.curve_plot_extrapolated.setData(draw.time, draw.signal)


def update_error_graph(self):

    pass
