import threading
from modules.utility import print_debug
from modules import interface
from copy import copy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import numpy as np
import seaborn as sn

plt.rcParams['axes.facecolor'] = 'black'
plt.rc('axes', edgecolor='w')
plt.rc('xtick', color='w')
plt.rc('ytick', color='w')
plt.rcParams['axes.titlecolor'] = "white"
plt.rcParams['axes.labelcolor'] = "white"
plt.rcParams["figure.autolayout"] = True

# goodluck


def choices_def(self, choice):
    # max chunks is 99
    # max order is 9
    # max % is 25

    chunks = []
    orders = []
    overlap = []
    if choice == "No. Of Chunks":
        for c in range(1, 10):
            chunks.append(c)
        return chunks
    elif choice == "Poly. Order":
        for p in range(1, 10):
            orders.append(p)
        return orders
    elif choice == "% Overlap":
        for p in range(1, 10):
            overlap.append(p)
        return overlap
    else:
        print("DIDNOT CHOOSE ")


def select_error_x(self, x_type="No. Of Chunks"):
    self.x_type = x_type


def select_error_y(self, y_type="Poly. Order"):
    self.y_type = y_type


def percentage_error_function(self):
    # percentage_error between interpolated signal and original signal
    self.percentage_error = []

    for i in range(self.min_val, self.max_val):
        self.percentage_error_temp = []
        for j in range(self.min_val, self.max_val):
            print("x=")
            print(i)
            print("y=")
            print(j)
            original_signal_avg = np.average(
                self.signal_processor_error.original_signal.magnitude)
            print("original_signal_avg:")
            print(original_signal_avg)
            interpolated_signal_avg = np.average(
                self.interpolated_signal_mag[i][j])
            print("interpolated_signal_avg:")
            print(interpolated_signal_avg)

            self.percentage_error_temp.append(
                (np.absolute(interpolated_signal_avg-original_signal_avg / original_signal_avg)))
        self.percentage_error.append(self.percentage_error_temp)
        print("there")
    print("percentage_error:")
    print(self.percentage_error)


def normalization(self):
    self.normalized_error = []

    for i in range(self.min_val, self.max_val):
        self.normalized_error_temp = []
        for j in range(self.min_val, self.max_val):
            value = (self.percentage_error[i][j] - np.amin(self.percentage_error)) / (
                np.amax(self.percentage_error) - np.amin(self.percentage_error))
            self.normalized_error_temp.append(value)
        self.normalized_error.append(self.normalized_error_temp)


def enter(self, order=1, chunks=1, percentage=9):
    self.signal_processor_error.interpolation_order = order
    self.signal_processor_error.max_chunks = chunks
    self.signal_processor_error.overlap_percent = percentage


def type(self, x_type, y_type):
    pass


def error_map(self):
    print_debug("error map assigned to thread: {}".format(
        threading.current_thread().name))
    t1 = threading.Thread(target=calculate_error,
                          args=(self,), name='error map thread')
    # start threads
    t1.start()
    # wait until threads finish their job
    t1.join()


def calculate_error(self, loading_counter: int = 0):
    # progress bar
    # TODO: both axis should be same size
    # values  and type of axis
    # for loop to get interpolated
    # put in array
    # compare original and interpolated
    print_debug("calculate error assigned to thread: {}".format(
        threading.current_thread().name))

    self.interpolated_signal_mag = []

    self.x_values = choices_def(self, choice=self.x_type)

    self.y_values = choices_def(self, choice=self.y_type)

    x = self.x_values
    y = self.y_values

    self.min_val = min(self.x_values)-1
    self.max_val = max(self.x_values)
    print(self.min_val)
    print(self.max_val)
    print("x_values:")
    print(self.x_values)

    print("x_type:")
    print(self.x_type)

    print("y_values:")
    print(self.y_values)

    print("y_type:")
    print(self.y_type)

    self.signal_processor_error = copy(self.signal_processor)
    self.signal_processor_error.interpolation_type = "spline"
    interface.progressBar_update(self, 1)
    for i in x:
        # to iterate on the y ranges
        self.interpolated_signal_temp = []
        for j in y:
            # intrapolate according to the 2 numbers and add to the matrix

            # order,chunks,percentage
            if (self.y_type == "No. Of Chunks" and self.x_type == "Poly. Order"):
                enter(self, order=i, chunks=j)

            elif (self.y_type == "Poly. Order" and self.x_type == "No. Of Chunks"):
                enter(self, order=j, chunks=i)

            elif (self.y_type == "No. Of Chunks" and self.x_type == "% Overlap"):
                enter(self, chunks=j, percentage=i)

            elif(self.y_type == "% Overlap" and self.x_type == "Poly. Order"):
                enter(self, order=i, percentage=j)

            elif(self.y_type == "Poly. Order" and self.x_type == "% Overlap"):
                enter(self, order=j, percentage=i)

            elif(self.y_type == "% Overlap" and self.x_type == "No. Of Chunks"):
                enter(self, chunks=i, percentage=j)

            else:
                print("seriously 3adat kol dah!!")

            print("x=")
            print(i)
            print("y=")
            print(j)
            self.signal_processor_error.interpolate()
            print("the interpolted signal magnitudes:")
            print(self.signal_processor_error.interpolated_signal.magnitude)
            self.interpolated_signal_temp.append(
                self.signal_processor_error.interpolated_signal.magnitude)

        self.interpolated_signal_mag.append(self.interpolated_signal_temp)
    interface.progressBar_update(self, 2)

    percentage_error_function(self)

    normalization(self)
    interface.progressBar_update(self, 3)

    plot_error_map(self, self.normalized_error, self.x_type, self.y_type)
    # multithreading
    # https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
    pass


def update_error_graph(self):

    pass


def create_error_map_figure(self):
    self.figure = plt.figure()
    self.figure.patch.set_facecolor('black')
    self.axes = self.figure.add_subplot()
    self.ErrorMap = Canvas(self.figure)
    self.error_plot_box.addWidget(self.ErrorMap)
    # plot_error_map(self) # CALL WHEN ERROR_BUTTON IS CLICKED INSTEAD


def plot_error_map(self, data=[], xlabel='', ylabel=''):

    self.axes.clear()
    plt.clf()


# plotting the heatmap
    erorr_map = sn.heatmap(data=data)


# displaying the plotted heatmap
    # plt.show()

    plt.title('Error Map')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    self.ErrorMap.draw()
    self.figure.canvas.draw()
