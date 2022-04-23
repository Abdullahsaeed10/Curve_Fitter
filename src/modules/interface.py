# OLD CODE.. REMOVE THIS COMMENT WHEN DONE MODIFYING

from ctypes import util
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTabWidget, QProgressBar, QMessageBox, QAction, QPushButton, QSlider, QComboBox, QLCDNumber, QStackedWidget, QStackedLayout, QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QDial, QLabel, QGridLayout, QToolButton
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from modules import openfile
from modules.utility import print_debug, print_log
import math


def about_us(self):
    QMessageBox.about(
        self, ' About ', 'This is a musical instruments emphasizer and a digital audio workstation \nCreated by junior students from the faculty of Engineering, Cairo University, Systems and Biomedical Engineering department \n \nTeam members: \n-Mohammed Nasser \n-Abdullah Saeed \n-Zeyad Mansour \n-Mariam Khaled \n \nhttps://github.com/mo-gaafar/Mini_Music_Workstation.git')

def toggle_residuals_plot(self):
    if self.residuals_button.isChecked():
        self.residuals_plot.hide()
        self.residuals_button.setDown(True)
    else:
        self.residuals_plot.show()

def toggle_fit_mode(self, MODE):
    if MODE == 'Chunk':
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

    # self.selection_tabWidget = self.findChild(
    #     QTabWidget, "selection_tabWidget")
    # self.selection_tabWidget.currentChanged.connect(
    #     lambda:  update_current_tab_index(self, self.selection_tabWidget.currentIndex()))

    ''' Menu Bar'''
    self.actionOpen = self.findChild(QAction, "actionOpen")
    self.actionOpen.triggered.connect(
        lambda: openfile.browse_window(self))

    # self.actionAbout_us = self.findChild(QAction, "actionAbout_Us")
    # self.actionAbout_us.triggered.connect(
    #     lambda: about_us(self))

    # # play button
    # self.play_pushButton = self.findChild(QPushButton, "play_pushButton")
    # self.play_pushButton.clicked.connect(
    #     lambda: emphasizer.play(self))
    pass
