# OLD CODE... REMOVE THIS COMMENT WHEN DONE MODIFYING
# TODO: should import wfdb and csv

from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
import numpy as np

from modules.utility import print_debug
from modules.curvefit import *
from modules import curvefit
import wfdb
import csv


def browse_window(self):
    self.graph_empty = False
    self.filename = QFileDialog.getOpenFileName(
        None, 'open the signal file', './', filter="Raw Data(*.hea *.dat *.csv *.txt *.xls)")
    path = self.filename[0]
    print_debug("Selected path: " + path)
    open_file(self, path)
    # play the sound

# shows the sound waves


def open_file(self, path):
    temp_time = []
    temp_magnitude = []
    temp_fsample = 0

    filetype = path[-3:]

    if filetype == "rec" or filetype == "dat" or filetype == "hea":

        # open wfdb file
        self.record = wfdb.rdrecord(path[:-4], channels=[0])

        # update signal object
        temp_magnitude = np.concatenate(
            self.record.p_signal)

        self.signal = Signal(signal=temp_magnitude, fsample=self.record.fs)

    if filetype == "csv" or filetype == "txt" or filetype == "xls":
        with open(path, 'r') as csvFile:    # 'r' its a mode for reading and writing
            csvReader = csv.reader(csvFile, delimiter=',')
            for line in csvReader:
                temp_magnitude.append(
                    float(line[1]))
                temp_time.append(float(line[0]))

    print_debug("Record loaded")
    curvefit.update_graph(self)
