import numpy as np


class Signal():
    def __init__(self, signal=[], fsample=0, time=[]) -> None:
        self.signal = signal
        self.fsample = fsample
        self.time = np.arange(0, len(signal)) / fsample

# how to deal with extrapolation???????????


class InterpolatedSignal(Signal):
    def __init__(self, signal=[], fsample=0) -> None:
        super().__init__(signal, fsample)
        self.interpolated_signal = self.interpolate(self.signal)

    def interpolate(self):
        pass

    def generate_error_map(self):
        # prograss bar

        # multithreading
        # https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
        pass

    def draw_error_equation(self):
        pass
