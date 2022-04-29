from modules.utility import print_debug
import numpy as np
from copy import copy
import sympy

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas

plt.rc('mathtext', fontset='cm')


class Signal():
    """Represents a signal"""

    def __init__(self, magnitude=[], fsample=0, time=[], coef=[]) -> None:

        self.magnitude = magnitude
        self.fsample = fsample
        self.time = time

        if self.fsample == 0:
            self.time = time
            if len(time) != 0:
                self.fsample = len(self.magnitude)/time[-1]

        if len(time) == 0:
            if len(magnitude) != 0:
                print_debug("Time axis auto generated")
                self.time = np.arange(0, len(magnitude))/fsample
            else:
                self.time = []

        # if (self.magnitude != [] and self.time == []) or (self.magnitude == [] and self.time != []):
        #     raise Exception("Signal must have a time or fsampling vector")

        self.coefficients = coef

    def __len__(self):
        """Returns the length of the signal"""
        if self.magnitude != []:
            return len(self.magnitude)
        else:
            print_debug("Signal has 0 length")
            return 0

    def __getitem__(self, index):
        """Returns the signal at the given index"""
        return copy(Signal(self.magnitude[index], self.fsample, self.time[index]))

    def __subtract__(self, other):
        """Subtracts two signals"""
        if self.fsample == other.fsample:
            return Signal(self.magnitude - other.magnitude, self.fsample, self.time)
        else:
            raise Exception("Signals must have the same sampling frequency")

    def set_max_samples(self, max_samples):
        """Sets the maximum number of samples"""
        if len(self.magnitude) > max_samples:
            self.magnitude = self.magnitude[:max_samples]
            self.time = self.time[:max_samples]

    def __append__(self, other):
        """Appends two signals"""
        if self.fsample == other.fsample:
            return copy(Signal(self.magnitude + other.magnitude, self.fsample, self.time + other.time))
        else:
            raise Exception("Signals must have the same sampling frequency")

    def clip(self, direction, percentage):
        """Clips the signal"""
        percentage = percentage / 100
        if direction == "left":
            self.magnitude = self.magnitude[int(
                len(self.magnitude) * (1 - percentage)):]
            self.time = self.time[int(len(self.time) * (1 - percentage)):]
        elif direction == "right":
            self.magnitude = self.magnitude[:int(
                len(self.magnitude) * (1 - percentage))]
            self.time = self.time[:int(len(self.time) * (1 - percentage))]
        else:
            raise Exception("Direction must be left or right")

    def set_data(self, magnitude, time):
        """Sets the magnitdue and time of the signal"""
        self.magnitude = magnitude
        self.time = time
        if len(self.magnitude) != len(self.time):
            raise Exception("Signal must have the same length")
        if len(self.magnitude) != 0:
            self.fsample = len(self.magnitude)/time[-1]

    def set_coefficients(self, coef):
        self.coefficients = coef

    def get_coefficients(self):
        return self.coefficients


class ChunkedSignal(Signal):
    """Represents a chunked signal"""

    def __init__(self, signal, max_chunks: int = 0, overlap_percent: int = 0) -> None:
        super().__init__(signal.magnitude, signal.fsample, signal.time)

        self.chunk_array = []
        """Array of full chunk signal objects (includes overlap)"""
        self.chunk_length = 0
        self.overlap_percent = overlap_percent
        if len(signal.magnitude) > 0:
            self.update_chunk_size(max_chunks)
            # self.generate_chunks()

    def update_chunk_size(self, max_chunks):
        self.chunk_length = int(len(self.magnitude)/max_chunks)
        print_debug("Chunk length: " + str(self.chunk_length))
        print_debug("Overlap percent: " + str(self.overlap_percent))
        self.overlap_length = round(
            self.chunk_length * (self.overlap_percent/100))  # TODO: FIX THIS
        self.generate_chunks()

    def merge_chunks(self):
        """Merges chunks into the main signal"""

        # TODO: Overlap averaging?

        # THIS IS A PLACEHOLDER: ignores overlap
        # clear data
        self.time = []
        self.magnitude = []

        for index in range(0, len(self.chunk_array)):
            print_debug("Merging chunk " + str(index))
            print_debug(self.chunk_array[index])
            print_debug("Time Data" + str(self.chunk_array[index].time))
            self.time.append(self.get_chunk_without_overlap(index).time)
            self.magnitude.append(
                self.get_chunk_without_overlap(index).magnitude)

        # Convert to 1D arrays
        self.time = np.concatenate(self.time)
        self.magnitude = np.concatenate(self.magnitude)

    def get_overlap(self, chunk_index, direction="left"):
        # TODO: should account for first index and last index chunks
        """Returns the overlap of the chunk"""
        overlap_length = self.overlap_length
        return self.chunk_array[chunk_index][-overlap_length:]

    def get_chunk(self, index):
        """Returns the chunk at the given index"""
        return self.chunk_array[index]

    def get_chunk_without_overlap(self, index):
        """Returns the chunk without overlap"""
        output = copy(self.chunk_array[index]
                      [:self.chunk_length-self.overlap_length])
        print_debug(" Chunk without overlap" + str(output))
        return output

    def get_coefficients(self, index=0):
        """Returns the coefficients of the chunk at the given index"""
        return self.chunk_array[index].coefficients

    def set_chunk(self, chunk_index, signal):
        """Modifies a single chunk signal"""
        # TODO: add corner case
        # add signal object to chunk
        self.chunk_array[chunk_index] = signal
        # call update merged chunks
        self.merge_chunks()

    def generate_chunks(self):
        """Generates signal objects for each chunk + overlap"""

        # generate chunks
        chunk_array = []
        chunk_length = self.chunk_length
        overlap_length = self.overlap_length

        for index in range(0, len(self.magnitude), chunk_length):
            chunk_array.append(Signal(self.magnitude[index:index+chunk_length + overlap_length],
                                      self.fsample,
                                      self.time[index:index +
                                                chunk_length + overlap_length],
                                      self.coefficients))

        self.chunk_array = chunk_array


class SignalProcessor():
    def __init__(self, original=Signal()) -> None:

        self.original_signal = copy(original)

        self.clipped_signal = copy(original)
        self.clip_percentage = 100

        self.interpolation_type = None
        self.interpolation_order = 0
        self.max_chunks = 1
        self.overlap_percent = 0

        self.extrapolation_type = None

        self.interpolated_signal = copy(original)
        self.extrapolated_signal = copy(original)

    def init_interpolation(self, type: str = None, order: int = 1, N_chunks: int = 1, overlap_percent: int = 0):
        if type == None:
            raise Exception("Interpolation type must be set")

        self.interpolation_type = type
        self.interpolation_order = order
        if len(self.original_signal) != 0:
            self.max_chunks = N_chunks
            if N_chunks > 1:
                self.overlap_percent = overlap_percent
                self.update_chunks(N_chunks, overlap_percent)

        self.interpolate()

    def interpolate(self):
        type = self.interpolation_type
        input = self.clipped_signal

        if type == "polynomial":
            coef = np.polyfit(input.time,
                              input.magnitude,
                              self.interpolation_order)
            self.interpolated_signal = Signal(magnitude=np.polyval(
                coef, input.time), fsample=input.fsample, coef=coef)

        elif type == "spline":
            self.clipped_signal = ChunkedSignal(
                self.clipped_signal, self.max_chunks, self.overlap_percent)
            self.interpolated_signal = copy(self.clipped_signal)

            for chunk_index in range(len(self.clipped_signal.chunk_array)):
                input = self.clipped_signal.get_chunk(chunk_index)
                coef = np.polyfit(input.time,
                                  input.magnitude,
                                  self.interpolation_order)
                self.interpolated_signal.set_chunk(chunk_index, Signal(
                    magnitude=np.polyval(coef, input.time), fsample=input.fsample, coef=coef, time=input.time))
        else:
            raise Exception("Interpolation type must be polynomial or spline")

    def extrapolate(self):
        """Extrapolates remaining signal, starting from N of clipped to N of original"""
        self.extrapolation_type = self.interpolation_type  # placeholder for now

        N_clipped = len(self.clipped_signal)
        N_original = len(self.original_signal)

        """Processing Here"""
        # fitting the clipped signal
        if self.extrapolation_type == "polynomial":
            coef = self.interpolated_signal.coefficients
            self.extrapolated_values = np.polyval(
                coef, self.original_signal.time[N_clipped:N_original])

        elif self.extrapolation_type == "spline":
            # coefficients of last chunk
            coef = self.interpolated_signal.chunk_array[-1].coefficients
            self.extrapolated_values = np.polyval(
                coef, self.original_signal.time[N_clipped:N_original])
            pass

        """Output signal here"""
        self.extrapolated_signal = Signal(
            magnitude=self.extrapolated_values, time=self.original_signal.time[N_clipped:N_original])

    def set_clipping(self, clip_percentage: int = 0):
        if clip_percentage == 100:
            raise Exception("Clip percentage cant be 100%")

        self.clip_percentage = clip_percentage
        # Resets the clipped signal
        self.clipped_signal = copy(self.original_signal)
        self.clipped_signal.clip("right", self.clip_percentage)

    def update_chunks(self, max_chunks: int, overlap_percent: int = 0):
        """Converts clipped signal object to chunked signal object"""
        self.max_chunks = max_chunks
        self.clipped_signal = ChunkedSignal(
            self.clipped_signal, max_chunks, overlap_percent)

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


def update_graph(self):
    if self.signal_processor.original_signal != None:
        draw = self.signal_processor.original_signal
        self.curve_plot_ref.setData(draw.time, draw.magnitude)

    if self.signal_processor.isInterpolated():
        draw = self.signal_processor.interpolated_signal
        self.curve_plot_interpolated.setData(draw.time, draw.magnitude)

        if self.signal_processor.interpolation_type == "spline":
            draw = self.signal_processor.interpolated_signal.chunk_array[self.polynomial_equation_spinBox.value(
            )]
            self.curve_plot_selected_chunk.setData(draw.time, draw.magnitude)

    if self.signal_processor.isExtrapolated():
        draw = self.signal_processor.extrapolated_signal
        self.curve_plot_extrapolated.setData(draw.time, draw.magnitude)

    update_latex(self)


def update_latex(self):
    if self.signal_processor.interpolation_type == "spline":
        latex(self, self.signal_processor.interpolated_signal.get_coefficients(
            self.polynomial_equation_spinBox.value()))
        self.polynomial_equation_spinBox.setMaximum(
            self.chunk_number_spinBox.value() - 1)

        draw = self.signal_processor.interpolated_signal.chunk_array[self.polynomial_equation_spinBox.value(
        )]
        self.curve_plot_selected_chunk.setData(draw.time, draw.magnitude)

    else:
        latex(self, self.signal_processor.interpolated_signal.coefficients)


def create_latex_figure(self):
    self.fig = plt.figure()
    self.fig.patch.set_facecolor('None')
    self.Latex = Canvas(self.fig)
    self.latex_box.addWidget(self.Latex)


def latex(self, coef, fontsize=12):
    self.fig.clear()
    polynomial = np.poly1d(coef)
    x = sympy.symbols('x')
    formula = sympy.printing.latex(sympy.Poly(
        polynomial.coef.round(2), x).as_expr())
    self.fig.text(0, 0.1, '${}$'.format(formula),
                  fontsize=fontsize, color='white')
    self.fig.canvas.draw()
