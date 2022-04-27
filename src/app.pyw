# https://namingconvention.org/python/ use the pythonic naming convention here (friendly reminder)

from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTabWidget
from modules import interface
from modules import resources
from modules.curvefit import *
from modules import errormap
import numpy as np
from modules.utility import print_debug
import sys


class MainWindow(QtWidgets.QMainWindow):
    ''' This is the PyQt5 GUI Main Window'''

    def __init__(self, *args, **kwargs):
        ''' Main window constructor'''

        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./resources/curvefittingwindow.ui', self)

        # set the title and icon
        self.setWindowIcon(QtGui.QIcon('./resources/icons/icon.png'))
        self.setWindowTitle("Curve Fitter")

        print_debug("Connectors Initialized")

        # initialize arrays and variables
        self.signal = Signal()
        self.signal_processor = SignalProcessor()

        # initialize interface components
        interface.init_plots(self)
        interface.init_connectors(self)


def main():

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
