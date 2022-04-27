
from turtle import width
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSpinBox, QProgressBar, QMessageBox, QAction, QPushButton, QSlider, QComboBox, QLCDNumber, QStackedWidget, QStackedLayout, QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QDial, QLabel, QGridLayout, QToolButton
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from modules import openfile
from modules.curvefit import update_graph, update_latex
from modules.errormap import update_error_graph
from modules.utility import print_debug, print_log
from modules import errormap
import pyqtgraph as pg
import time 


def about_us(self):
    QMessageBox.about(
        self, ' About ', 'This is a musical instruments emphasizer and a digital audio workstation \nCreated by junior students from the faculty of Engineering, Cairo University, Systems and Biomedical Engineering department \n \nTeam members: \n-Mohammed Nasser \n-Abdullah Saeed \n-Zeyad Mansour \n-Mariam Khaled \n \nhttps://github.com/mo-gaafar/Mini_Music_Workstation.git')


def update_interpolation(self):

    print_debug("Updating Interpolation")

    if self.chunk_button.isChecked():
        order = int(self.polynomial_degree_spinBox.value())
        self.signal_processor.init_interpolation(
            type="polynomial", order=order)

    elif self.spline_button.isChecked():
        order = int(self.polynomial_degree_spinBox.value())
        chunk_number = int(self.chunk_number_spinBox.value())
        overlap_percent = int(self.overlap_spinBox.value())

        self.signal_processor.init_interpolation(
            type="spline",
            order=order,
            N_chunks=chunk_number,
            overlap_percent=overlap_percent)

    update_graph(self)


def update_extrapolation(self):
    self.signal_processor.extrapolate()

    update_graph(self)


def update_clipping(self):
    clipping = self.extrapolate_spinBox.value()
    print_debug("Clipping: " + str(clipping))
    self.signal_processor.set_clipping(clipping)
    print_debug("Signal length: " +
                str(len(self.signal_processor.clipped_signal)))
    update_interpolation(self)
    update_extrapolation(self)


def update_error(self):
    update_error_graph(self)


def toggle_error_plot(self):
    if self.error_button.isChecked():
        self.error_plot.hide()
        self.error_button.setDown(True)
    else:
        self.error_plot.show()


def toggle_fit_mode(self, mode):
    if mode == 'Chunk':
        if self.spline_button.isChecked():
            self.spline_button.setDown(False)
            self.spline_button.setChecked(False)
            self.spline_options_widget.hide()
            self.polynomial_equation_spinBox.hide()

        self.chunk_button.setDown(True)
        self.chunk_button.setChecked(True)

    else:
        if self.chunk_button.isChecked():
            self.chunk_button.setDown(False)
            self.chunk_button.setChecked(False)
            self.spline_options_widget.show()
            self.polynomial_equation_spinBox.show()

        self.spline_button.setDown(True)
        self.spline_button.setChecked(True)

######################## TODO: To be checked ########################

def progressBar_value(self):

    for i in range(100):
            time.sleep(0.00001)
            self.progressBar.setValue(i+1)
    return self.progressBar.value()


def init_plots(self):
    # initializing plot widgets

    pen = pg.mkPen(color=(150, 150, 150), width=2)
    self.curve_plot_ref = self.curve_plot.plot(pen=pen)

    pen = pg.mkPen(color=(255, 15, 10), width=2)
    self.curve_plot_interpolated = self.curve_plot.plot(pen=pen)

    pen = pg.mkPen(color=(15, 255, 10), style=QtCore.Qt.DotLine, width=2)
    self.curve_plot_extrapolated = self.curve_plot.plot(pen=pen)

    pen = pg.mkPen(color=(0,255,4), width=2)
    self.curve_plot_selected_chunk = self.curve_plot.plot(pen=pen)


def combobox_selections_visibility(self):
        view = self.y_comboBox.view()
        view.setRowHidden(self.hidden_row, False)
        view.setRowHidden(self.x_comboBox.currentIndex(), True)
        self.hidden_row = self.x_comboBox.currentIndex()

        self.y_comboBox.setCurrentIndex((self.hidden_row + 1) % 3)

def init_connectors(self):
    # '''Initializes all event connectors and triggers'''

    self.chunk_button = self.findChild(QToolButton, "chunk_button")
    self.chunk_button.setCheckable(True)
    self.chunk_button.setDown(True)
    self.chunk_button.setChecked(True)

    self.spline_options_widget.hide()
    self.polynomial_equation_spinBox.hide()
    self.chunk_button.clicked.connect(
        lambda: toggle_fit_mode(self, 'Chunk'))

    self.spline_button.setCheckable(True)
    self.spline_button.clicked.connect(
        lambda: toggle_fit_mode(self, 'Spline'))

    
    self.error_button.setCheckable(True)
    self.error_button.toggled.connect(
        lambda: toggle_error_plot(self))

    self.polynomial_degree_spinBox = self.findChild(
        QSpinBox, "polynomial_degree_spinBox")
    self.polynomial_degree_spinBox.valueChanged.connect(
        lambda: update_interpolation(self))

    self.extrapolate_spinBox = self.findChild(
        QSpinBox, "extrapolate_spinBox")
    self.extrapolate_spinBox.valueChanged.connect(
        lambda: update_clipping(self))

    self.chunk_number_spinBox = self.findChild(
        QSpinBox, "chunk_number_spinBox")
    self.chunk_number_spinBox.valueChanged.connect(
        lambda: update_interpolation(self))
    
    
    self.error_map_apply_button = self.findChild(QPushButton, "error_map_apply_button")
    self.error_map_apply_button.clicked.connect(
         lambda: errormap.calculate_error(self))
    
    self.x_comboBox.currentIndexChanged.connect(
        lambda: errormap.select_error_y(self, self.x_comboBox.currentText()))
    self.x_comboBox.currentIndexChanged.connect(
        lambda: combobox_selections_visibility(self))
    
    self.x_comboBox.currentIndexChanged.connect(
        lambda: errormap.select_error_x(self, self.x_comboBox.currentText()))

    self.y_comboBox.currentIndexChanged.connect(
        lambda: errormap.select_error_y(self, self.y_comboBox.currentText()))
    
    self.polynomial_equation_spinBox.valueChanged.connect(
        lambda: update_latex(self))
    
    view = self.y_comboBox.view()
    view.setRowHidden(0, True)

######################## TODO: add support for progress bar ########################
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

    pass
