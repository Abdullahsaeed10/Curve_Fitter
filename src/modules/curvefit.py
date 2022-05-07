from math import ceil
from modules.utility import print_debug
import numpy as np
from copy import copy
import sympy
from scipy import interpolate as interp
from modules.signals import Signal, ChunkedSignal

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas

plt.rc('mathtext', fontset='cm')


class SignalProcessor():
    def __init__(self, original=Signal()) -> None:

        self.original_signal = copy(original)

        self.clipped_signal = copy(original)
        self.clip_percentage = 100

        self.interpolation_type = None
        self.interpolation_order = 0
        self.max_chunks = 1
        self.overlap_percent = 0
        self.smoothing_factor = 0
        self.kernel = "thin_plate_spline"

        self.extrapolation_type = None

        self.interpolated_signal = copy(original)
        self.extrapolated_signal = copy(original)

    def init_interpolation(self, type: str = None, order: int = 1, N_chunks: int = 1,
                           overlap_percent: int = 0, smoothing_factor=0, kernel="thin_plate_spline"):
        self.interpolation_type = type
        self.interpolation_order = order
        self.smoothing_factor = smoothing_factor/100
        self.kernel = kernel
        if type == None:
            raise Exception("Interpolation type must be set")
        # TODO: Rethink updating to reduce code repetition
        if type == "polynomial" or "spline" or "rbf":
            if len(self.original_signal) != 0:
                self.max_chunks = N_chunks
                # Generates signal chunks
                if N_chunks > 1:
                    self.overlap_percent = overlap_percent
                    self.update_chunks(N_chunks, overlap_percent)

        self.interpolate()

    def interpolate(self):
        type = self.interpolation_type

        self.clipped_signal = ChunkedSignal(
            self.clipped_signal, self.max_chunks, self.overlap_percent)
        self.interpolated_signal = copy(self.clipped_signal)

        for chunk_index in range(len(self.clipped_signal.chunk_array)):
            input = self.clipped_signal.get_chunk(chunk_index)
            coef = []
            # processing interpolation
            if type == "polynomial":
                coef = np.polyfit(input.time,
                                  input.magnitude,
                                  self.interpolation_order)
                magnitude = np.polyval(coef, input.time)

            elif type == "spline":
                spl = interp.UnivariateSpline(input.time,
                                              input.magnitude,
                                              k=self.interpolation_order,
                                              s=self.smoothing_factor)
                magnitude = spl(input.time)

            elif type == "rbf":
                rbf = interp.RBFInterpolator(input.time,
                                             input.magnitude,
                                             kernel=self.kernel, degree=self.interpolation_order,
                                             smoothing=self.smoothing_factor)
                magnitude = rbf(input.time)
            elif type == "hermite":
                hermite = interp.PchipInterpolator(
                    input.time, input.magnitude, axis=0)
                magnitude = hermite(input.time)
            else:
                raise Exception(
                    "Interpolation type must be polynomial , spline or rbf")
                return
            # output
            self.interpolated_signal.set_chunk(chunk_index, Signal(
                magnitude=magnitude, fsample=input.fsample, coef=coef, time=input.time))

    def extrapolate(self):
        """Extrapolates remaining signal, starting from N of clipped to N of original"""
        self.extrapolation_type = self.interpolation_type  # placeholder for now

        N_clipped = len(self.clipped_signal)
        N_original = len(self.original_signal)

        """Processing Here"""
        # fitting the clipped signal
        if self.extrapolation_type == "spline":
            spl = interp.UnivariateSpline(self.clipped_signal.time,
                                          self.clipped_signal.magnitude,
                                          k=self.interpolation_order,
                                          s=self.smoothing_factor,
                                          ext=0)

            # plot remaining time
            self.extrapolated_values = spl(
                self.original_signal.time[N_clipped:N_original])

        elif self.extrapolation_type == "polynomial":
            # coefficients of last chunk
            coef = self.interpolated_signal.chunk_array[-1].coefficients
            self.extrapolated_values = np.polyval(
                coef, self.original_signal.time[N_clipped:N_original])

        elif self.extrapolation_type == "hermite":
            input = self.interpolated_signal.chunk_array[-1]
            hermite = interp.PchipInterpolator(input.time,
                                               input.magnitude,
                                               extrapolate=True)
            self.extrapolated_values = hermite(
                self.original_signal.time[N_clipped:N_original])

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

    def percentage_error(self):
        # signal1 is the original
        interpolated = self.interpolated_signal.magnitude
        original = self.original_signal.magnitude[0:len(interpolated)]

        self.sub = np.subtract(original, interpolated)

        original_minus_interpolated = np.average(np.absolute(self.sub))
        original_avg = np.average(original)

        self.percentageoferror = np.absolute(
            original_minus_interpolated / original_avg)*100
        return self.percentageoferror


def update_graph(self):
    if self.signal_processor.original_signal != None:
        draw = self.signal_processor.original_signal
        self.curve_plot_ref.setData(draw.time, draw.magnitude)

    if self.signal_processor.isInterpolated():
        draw = self.signal_processor.interpolated_signal
        self.curve_plot_interpolated.setData(draw.time, draw.magnitude)

        if type(self.signal_processor.interpolated_signal) == ChunkedSignal:
            draw = self.signal_processor.interpolated_signal.chunk_array[self.polynomial_equation_spinBox.value(
            )]
            self.curve_plot_selected_chunk.setData(draw.time, draw.magnitude)
        else:
            self.curve_plot_selected_chunk.setData([], [])

    if self.signal_processor.isExtrapolated():
        draw = self.signal_processor.extrapolated_signal
        self.curve_plot_extrapolated.setData(draw.time, draw.magnitude)

    update_latex(self)


def update_latex(self):
    if self.signal_processor.interpolation_type == "polynomial":
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
