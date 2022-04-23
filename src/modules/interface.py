# OLD CODE.. REMOVE THIS COMMENT WHEN DONE MODIFYING

from ctypes import util
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTabWidget, QProgressBar, QMessageBox, QAction, QPushButton, QSlider, QComboBox, QLCDNumber, QStackedWidget, QStackedLayout, QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QDial, QLabel, QGridLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from modules import openfile
from modules.utility import print_debug, print_log
import math


def about_us(self):
    QMessageBox.about(
        self, ' About ', 'This is a musical instruments emphasizer and a digital audio workstation \nCreated by junior students from the faculty of Engineering, Cairo University, Systems and Biomedical Engineering department \n \nTeam members: \n-Mohammed Nasser \n-Abdullah Saeed \n-Zeyad Mansour \n-Mariam Khaled \n \nhttps://github.com/mo-gaafar/Mini_Music_Workstation.git')


def init_connectors(self):
    # '''Initializes all event connectors and triggers'''

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
