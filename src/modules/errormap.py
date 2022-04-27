import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import numpy as np
import seaborn as sn

plt.rcParams['axes.facecolor'] = 'black'
plt.rc('axes', edgecolor='w')
plt.rc('xtick', color='w')
plt.rc('ytick', color='w')
plt.rcParams['axes.titlecolor'] = "white"
plt.rcParams["figure.autolayout"] = True

# goodluck

def calculate_error(self, loading_counter: int = 0):
    # progress bar

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
    plot_error_map(self) # CALL WHEN ERROR_BUTTON IS CLICKED INSTEAD


def plot_error_map(self, data = []):

    self.axes.clear()
     ############### RANDOM DATA TO TEST HEAT MAP #######################
    data = np.random.randint(low = 1,
                         high = 100,
                         size = (10, 10))
  #######################################################################

# plotting the heatmap
    erorr_map = sn.heatmap(data = data)
  
# displaying the plotted heatmap
    #plt.show()

    plt.title('Error Map')
    self.ErrorMap.draw()
    self.figure.canvas.draw()