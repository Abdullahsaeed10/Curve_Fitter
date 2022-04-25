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
