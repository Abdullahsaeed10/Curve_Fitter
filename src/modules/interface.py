
from turtle import width
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSpinBox, QProgressBar, QMessageBox, QAction, QPushButton, QSlider, QComboBox, QLCDNumber, QStackedWidget, QStackedLayout, QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QDial, QLabel, QGridLayout, QToolButton
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from matplotlib.pyplot import bar
from sympy import degree
from modules import openfile
from modules.curvefit import update_graph, update_latex
from modules.utility import print_debug, print_log
from modules import errormap
import pyqtgraph as pg
import time
import threading
import os


def about_us(self):
    QMessageBox.about(
        self, ' About ', 'This is a curve fitter \nCreated by junior students from the faculty of Engineering, Cairo University, Systems and Biomedical Engineering department \n \nTeam members: \n-Mohammed Nasser \n-Abdullah Saeed \n-Zeyad Mansour \n-Mariam Khaled \n \nhttps://github.com/mo-gaafar/Curve_Fitter.git')


def update_interpolation(self):

    print_debug("Updating Interpolation")
    chunk_number = int(self.chunk_number_spinBox.value())
    overlap_percent = int(self.overlap_spinBox.value())

    if self.polynomial_button.isChecked():
        order = int(self.polynomial_degree_spinBox.value())

        self.signal_processor.init_interpolation(
            type="polynomial",
            order=order,
            N_chunks=chunk_number,
            overlap_percent=overlap_percent)

    elif self.spline_button.isChecked():
        smoothing_factor = int(self.smoothing_spinBox.value())
        order = int(self.polynomial_degree_spinBox.value())
        self.signal_processor.init_interpolation(
            type="spline",
            smoothing_factor=smoothing_factor,
            order=order,
            N_chunks=chunk_number,
            overlap_percent=overlap_percent)

    elif self.hermite_button.isChecked():
        smoothing_factor = int(self.smoothing_spinBox.value())
        order = int(self.polynomial_degree_spinBox.value())
        self.signal_processor.init_interpolation(
            type="hermite",
            smoothing_factor=smoothing_factor,
            order=order,
            N_chunks=chunk_number,
            overlap_percent=overlap_percent)

    self.signal_processor.extrapolate()
    update_error_label(self)
    update_graph(self)


def update_clipping(self):
    clipping = self.extrapolate_spinBox.value()
    print_debug("Clipping: " + str(clipping))
    self.signal_processor.set_clipping(clipping)
    print_debug("Signal length: " +
                str(len(self.signal_processor.clipped_signal)))
    update_interpolation(self)
    # update_extrapolation(self)


def update_error_label(self):
    self.percentage_error_label.setNum(
        (self.signal_processor.percentage_error()))


def update_error(self):
    errormap.plot_error_map(self)


def toggle_error_plot(self):
    if self.error_button.isChecked():
        self.error_plot.hide()
        self.error_button.setDown(True)
    else:
        self.error_plot.show()


def toggle_fit_mode(self, mode):
    if mode == 'Polynomial':
        if self.spline_button.isChecked() | self.hermite_button.isChecked():
            self.spline_button.setDown(False)
            self.spline_button.setChecked(False)
            self.hermite_button.setDown(False)
            self.hermite_button.setChecked(False)
            self.smoothing_options.hide()
            self.chunks_options.show()
            self.polynomial_options.show()
            self.polynomial_degree_spinBox.setMaximum(9)
            self.polynomial_degree_spinBox.setMinimum(0)

        self.polynomial_button.setDown(True)
        self.polynomial_button.setChecked(True)

    elif mode == 'Spline':
        if self.polynomial_button.isChecked() | self.hermite_button.isChecked():
            self.polynomial_button.setDown(False)
            self.polynomial_button.setChecked(False)
            self.hermite_button.setDown(False)
            self.hermite_button.setChecked(False)
            self.smoothing_options.show()
            self.chunks_options.show()
            self.polynomial_options.show()
            self.polynomial_degree_spinBox.setMaximum(5)
            self.polynomial_degree_spinBox.setMinimum(1)

        self.spline_button.setDown(True)
        self.spline_button.setChecked(True)

    else:
        if self.polynomial_button.isChecked() | self.spline_button.isChecked():
            self.polynomial_button.setDown(False)
            self.polynomial_button.setChecked(False)
            self.spline_button.setDown(False)
            self.spline_button.setChecked(False)
            self.smoothing_options.hide()
            self.chunks_options.show()
            self.polynomial_options.hide()
            self.polynomial_degree_spinBox.setMaximum(3)
            self.polynomial_degree_spinBox.setValue(3)
            self.polynomial_degree_spinBox.setMinimum(3)

        self.hermite_button.setDown(True)
        self.hermite_button.setChecked(True)

    update_interpolation(self)
# BUG: Threading causes crash


# def progressBar_update(self, x, y):
#     self.cancel_button.show()
#     self.progressBar.show()

#     if x == 1:
#         for i in range(20):
#             #time.sleep(1)
#             self.progressBar.setValue(i+1)
#         return self.progressBar.value()
#     elif x == 2:
#         #for i in range(20, 100):

#             #time.sleep(1)
#             self.progressBar.setValue(y+1)
#             if (y==100):  
#                 self.progressBar.hide()
#                 self.cancel_button.hide()
#             return 
#     elif x == 3:
#         for i in range(80, 100):

#             time.sleep(0.1)
#             self.progressBar.setValue(i+1)
#         self.progressBar.hide()
#         self.cancel_button.hide()
#         return self.progressBar.value()

def progressBar_update(self, barpercent):
    self.startLoading.emit()
    print_debug("Progress bar update: " + str(barpercent))
    print_debug("bar percent " + str(barpercent))
   
    for self.current_progressBar  in range(barpercent):
        self.progressChanged.emit(self.current_progressBar+1)
        self.current_progressBar += 1
        if ( self.current_progressBar==100):
            print_debug("the barpercent has reached 100 and enter the endLoading")
            self.endLoading.emit()
            return
    return self.current_progressBar
# def progressBar_update(self, x):
#     self.startLoading.emit()
#     if x == 1:
#         for i in range(50):
#             time.sleep(0.01)
#             # self.progressBar.setValue(i+1)
#             self.progressChanged.emit(i+1)
#         return
#     elif x == 2:
#         for i in range(50, 80):

#             time.sleep(0.01)
#             # self.progressBar.setValue(i+1)
#             self.progressChanged.emit(i+1)
#         return
#     elif x == 3:
#         for i in range(80, 100):

#             time.sleep(0.1)
#             # self.progressBar.setValue(i+1)
#             self.progressChanged.emit(i+1)
#         # self.progressBar.hide()
#         # self.cancel_button.hide()
#         self.endLoading.emit()  # connects to stop_progressBar
#         return


def start_progressBar(self):
    self.cancel_button.show()
    self.progressBar.show()

def finished_progressBar(self):
    self.progressBar.hide()
    self.cancel_button.hide()

def stop_progressBar(self):
    print_debug("Stopping progress bar")
    self.toggle_progressBar = 1
    # x=self.progressBar.value()
    # self.progressBar.setValue(x)
    self.progressBar.hide()
    self.cancel_button.hide()


def init_plots(self):
    # initializing plot widgets

    pen = pg.mkPen(color=(150, 150, 150), width=2)
    self.curve_plot_ref = self.curve_plot.plot(pen=pen)

    pen = pg.mkPen(color=(255, 15, 10), width=2)
    self.curve_plot_interpolated = self.curve_plot.plot(pen=pen)

    pen = pg.mkPen(color=(15, 255, 10), style=QtCore.Qt.DotLine, width=2)
    self.curve_plot_extrapolated = self.curve_plot.plot(pen=pen)

    pen = pg.mkPen(color=(200, 200, 0), width=3)
    self.curve_plot_selected_chunk = self.curve_plot.plot(pen=pen)


def combobox_selections_visibility(self):
    view = self.y_comboBox.view()
    view.setRowHidden(self.hidden_row, False)
    view.setRowHidden(self.x_comboBox.currentIndex(), True)
    self.hidden_row = self.x_comboBox.currentIndex()

    self.y_comboBox.setCurrentIndex((self.hidden_row + 1) % 3)


def init_connectors(self):
    # '''Initializes all event connectors and triggers'''

    self.polynomial_button.setCheckable(True)
    self.polynomial_button.setDown(True)
    self.polynomial_button.setChecked(True)

    # this is a signal that is emitted by the thread
    self.progressChanged.connect(self.progressBar.setValue)
    self.endLoading.connect(lambda: finished_progressBar(self))
    self.startLoading.connect(lambda: start_progressBar(self))

    self.progressBar.hide()
    self.cancel_button.hide()

    self.smoothing_options.hide()
    self.polynomial_button.clicked.connect(
        lambda: toggle_fit_mode(self, 'Polynomial'))

    self.spline_button.setCheckable(True)
    self.spline_button.clicked.connect(
        lambda: toggle_fit_mode(self, 'Spline'))

    self.hermite_button.setCheckable(True)
    self.hermite_button.clicked.connect(
        lambda: toggle_fit_mode(self, 'RBF'))

    self.error_button.setCheckable(True)
    self.error_button.toggled.connect(
        lambda: toggle_error_plot(self))

    self.polynomial_degree_spinBox = self.findChild(
        QSpinBox, "polynomial_degree_spinBox")
    self.polynomial_degree_spinBox.valueChanged.connect(
        lambda: update_interpolation(self))

    self.overlap_spinBox.valueChanged.connect(
        lambda: update_interpolation(self))

    self.smoothing_spinBox.valueChanged.connect(
        lambda: update_interpolation(self))

    self.extrapolate_spinBox = self.findChild(
        QSpinBox, "extrapolate_spinBox")
    self.extrapolate_spinBox.valueChanged.connect(
        lambda: update_clipping(self))

    self.chunk_number_spinBox = self.findChild(
        QSpinBox, "chunk_number_spinBox")
    self.chunk_number_spinBox.valueChanged.connect(
        lambda: update_interpolation(self))

    self.error_map_apply_button = self.findChild(
        QPushButton, "error_map_apply_button")
    self.error_map_apply_button.clicked.connect(
        lambda: errormap.error_map(self))

    self.cancel_button = self.findChild(QPushButton, "cancel_button")
    self.cancel_button.clicked.connect(
        lambda: stop_progressBar(self))

    self.x_comboBox.currentIndexChanged.connect(
        lambda: errormap.select_error_x(self, self.x_comboBox.currentText()))

    self.x_comboBox.currentIndexChanged.connect(
        lambda: combobox_selections_visibility(self))

    self.y_comboBox.currentIndexChanged.connect(
        lambda: errormap.select_error_y(self, self.y_comboBox.currentText()))

    self.polynomial_equation_spinBox.valueChanged.connect(
        lambda: update_latex(self))

    view = self.y_comboBox.view()
    view.setRowHidden(0, True)

    # percentage error extra intra

    percentage_error_label = self.findChild(QLabel, "percentage_error_label")

    # TODO: Add support for progress bar
    # self.progressBar = self.findChild(QProgressBar, "progressBar")
    # self.triggered.connect(
    #     lambda: progressBar_value(self))

    ''' Menu Bar'''
    self.actionOpen = self.findChild(QAction, "actionOpen")
    self.actionOpen.triggered.connect(
        lambda: openfile.browse_window(self))

    # self.actionAbout_us = self.findChild(QAction, "actionAbout_Us")
    # self.actionAbout_us.triggered.connect(
    #     lambda: about_us(self))
    self.actionAbout_us = self.findChild(QAction, "actionAbout_Us")
    self.actionAbout_us.triggered.connect(
        lambda: about_us(self))
    pass
