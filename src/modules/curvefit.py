import numpy as np
from numpy import fft


class Signal():
    def __init__(self, signal=[], fsample=0, time=[]) -> None:
        self.signal = signal
        self.fsample = fsample

        if self.fsample == 0:
            self.time = time
            if len(time) != 0:
                self.fsample = time[-1]/len(self.signal)
        else:
            self.time = np.arange(0, len(signal)) / fsample
        pass

    # operator overload
    def __subtract__(self, other):
        if self.fsample == other.fsample:
            return Signal(self.signal - other.signal, self.fsample, self.time)

    # divide signal into chunks
    def chunk(self, chunk_size):
        return [self.signal[i:i + chunk_size] for i in range(0, len(self.signal), chunk_size)]


class Processing():
    def __init__(self, original=Signal()) -> None:
        self.original_signal = original
        self.modified_signal = original
        pass

    def reset_signal(self):
        self.modified_signal = self.original_signal
        pass

    def interpolate(self):
        pass

    def extrapolate(self):
        pass

    def calculate_error(self):
        pass

    def draw_error_equation(self):
        pass


def update_graph(self):
    self.curve_plot.plot(self.signal.time, self.signal.signal)
    pass


def update_error(self):
    # prograss bar

    # multithreading
    # https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
    pass
