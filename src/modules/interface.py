# OLD CODE.. REMOVE THIS COMMENT WHEN DONE MODIFYING

from ctypes import util
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSpinBox, QProgressBar, QMessageBox, QAction, QPushButton, QSlider, QComboBox, QLCDNumber, QStackedWidget, QStackedLayout, QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QDial, QLabel, QGridLayout, QToolButton
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from modules import openfile
from modules.curvefit import update_graph
from modules.utility import print_debug, print_log


def about_us(self):
    QMessageBox.about(
        self, ' About ', 'This is a musical instruments emphasizer and a digital audio workstation \nCreated by junior students from the faculty of Engineering, Cairo University, Systems and Biomedical Engineering department \n \nTeam members: \n-Mohammed Nasser \n-Abdullah Saeed \n-Zeyad Mansour \n-Mariam Khaled \n \nhttps://github.com/mo-gaafar/Mini_Music_Workstation.git')


def update_interpolation(self):
    """Creates Interpolation object based on user input"""

    print_debug("Updating Interpolation")

    clipping = self.extrapolate_spinBox.value()
    print_debug("Clipping: " + str(clipping))
    self.signal_processor.set_clipping(clipping)
    print_debug("Signal length: " + str(len(self.signal_processor.clipped_signal)))

    if self.chunk_button.isChecked():
        order = int(self.polynomial_degree_spinBox.value())
        self.signal_processor.init_interpolation(
            interpolation_type="polynomial", interpolation_order=order)
        

    elif self.spline_button.isChecked():
        order = int(self.spline_order_comboBox.currentText())
        # TODO:add spline interpolation

    update_graph(self)


def toggle_residuals_plot(self):
    if self.residuals_button.isChecked():
        self.residuals_plot.hide()
        self.residuals_button.setDown(True)
    else:
        self.residuals_plot.show()


def toggle_fit_mode(self, mode):
    if mode == 'Chunk':
        if self.spline_button.isChecked():
            self.spline_button.setDown(False)
            self.spline_button.setChecked(False)
            self.spline_options_widget.hide()

        self.chunk_button.setDown(True)
        self.chunk_button.setChecked(True)

    else:
        if self.chunk_button.isChecked():
            self.chunk_button.setDown(False)
            self.chunk_button.setChecked(False)
            self.spline_options_widget.show()

        self.spline_button.setDown(True)
        self.spline_button.setChecked(True)


def init_connectors(self):
    # '''Initializes all event connectors and triggers'''

    self.chunk_button = self.findChild(QToolButton, "chunk_button")
    self.chunk_button.setCheckable(True)
    self.chunk_button.setDown(True)
    self.chunk_button.setChecked(True)

    self.spline_options_widget.hide()
    self.chunk_button.clicked.connect(
        lambda: toggle_fit_mode(self, 'Chunk'))

    self.spline_button.setCheckable(True)
    self.spline_button.clicked.connect(
        lambda: toggle_fit_mode(self, 'Spline'))

    #self.residuals_button = self.findChild(QPushButton, "residuals_button")
    self.residuals_button.setCheckable(True)
    self.residuals_button.toggled.connect(
        lambda: toggle_residuals_plot(self))

    self.polynomial_degree_spinBox = self.findChild(
        QSpinBox, "polynomial_degree_spinBox")
    self.polynomial_degree_spinBox.valueChanged.connect(
        lambda: update_interpolation(self))

    self.extrapolate_spinBox = self.findChild(
        QSpinBox, "extrapolate_spinBox")
    self.extrapolate_spinBox.valueChanged.connect(
        lambda: update_interpolation(self))

    ''' Menu Bar'''
    self.actionOpen = self.findChild(QAction, "actionOpen")
    self.actionOpen.triggered.connect(
        lambda: openfile.browse_window(self))

    # self.actionAbout_us = self.findChild(QAction, "actionAbout_Us")
    # self.actionAbout_us.triggered.connect(
    #     lambda: about_us(self))

    pass
