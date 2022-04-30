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
import numpy as np
from copy import copy

from modules.utility import print_debug


def values(self):
    # whether what the user chose it will still be the same no. for both axes 
    vals=[]                       
    for v in range (1,10):
        vals.append(v)
    return vals
   


def select_error_x (self,x_type="No. Of Chunks"):
    self.x_type=x_type
    
    

   
    
def select_error_y (self,y_type="Poly. Order"):
    self.y_type=y_type
    
    
def percentage_error_function(self):
    # percentage_error between interpolated signal and original signal
    self.percentage_error=[]
    for i in range(self.min_val,self.max_val):
        self.percentage_error_temp=[]
        for j in range(self.min_val,self.max_val):
            N_clipped = len(self.interpolated_signal_mag[i][j])
            N_original = len(self.signal_processor_error.original_signal)
            print(len(self.signal_processor_error.original_signal.magnitude[:N_clipped]))
            print(len(self.interpolated_signal_mag[i][j]))
            percentage_value=self.signal_processor_error.percentage_error(self.signal_processor_error.original_signal.magnitude[:N_clipped],self.interpolated_signal_mag[i][j])
         
            self.percentage_error_temp.append(percentage_value)
        self.percentage_error.append(self.percentage_error_temp)
        print("there")
    print("percentage_error:")
    print(self.percentage_error)


def normalization(self):
    self.normalized_error=[]
    
    for i in range(self.min_val,self.max_val):
        self.normalized_error_temp=[]
        for j in range(self.min_val,self.max_val):
            value=(self.percentage_error[i][j] - np.amin(self.percentage_error)) / (np.amax(self.percentage_error) - np.amin(self.percentage_error))
            print("value:")
            print(value)
            self.normalized_error_temp.append(value)
        self.normalized_error.append(self.normalized_error_temp)
        print("NORM")
    print("NORMALIZED:")
    print(self.normalized_error[0])
    print(self.normalized_error[1])


def enter(self,order=1,chunks=1,percentage=9):
    self.signal_processor_error.interpolation_order=order
    self.signal_processor_error.max_chunks=chunks
    self.signal_processor_error.overlap_percent=percentage
    print("overlap")
    print(self.signal_processor_error.overlap_percent)

    
def type_selection(self,x_type,y_type,i,j):
    #order,chunks,percentage
    self.y_type==y_type
    self.x_type==x_type
    if ((self.y_type=="No. Of Chunks" and self.x_type=="Poly. Order") or (self.y_type=="Poly. Order" and self.x_type=="No. Of Chunks")) :
        enter(self,order=i,chunks=j)

    elif ((self.y_type=="No. Of Chunks" and self.x_type=="% Overlap") or (self.y_type=="% Overlap" and self.x_type=="No. Of Chunks" )):
        enter(self,chunks=i,percentage=j)

    elif((self.y_type=="% Overlap" and self.x_type=="Poly. Order")or (self.y_type=="Poly. Order" and self.x_type=="% Overlap" )):
        enter(self,order=i,percentage=j)
    else:
        print("seriously 3adat kol dah!!")




def calculate_error(self, loading_counter: int = 0):
    # progress bar
    # TODO: both axis should be same size
    # values  and type of axis
    # for loop to get interpolated 
    # put in array
    # compare original and interpolated
    self.signal_processor_error=copy(self.signal_processor)
    self.signal_processor_error.interpolation_type= "spline"
    if (self.signal_processor_error.interpolation_type== "polynomial"):
        raise Exception("Interpolation type has no error map")
    self.interpolated_signal_mag=[]
  
    self.x_values=values(self)

    self.y_values=values(self)

    x=self.x_values
    y=self.y_values
    
    self.min_val=min(self.x_values)-1
    self.max_val=max(self.x_values)
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


    for i in x:
    # to iterate on the y ranges
        self.interpolated_signal_temp=[]
        for j in y:
        # intrapolate according to the 2 numbers and add to the matrix
            
        #order,chunks,percentage
            
            type_selection(self,self.x_type,self.y_type,i,j) 
            print("x=")
            print(i)
            print("y=")
            print(j)
            self.signal_processor_error.interpolate() 
            print("the interpolted signal magnitudes:")
            print(self.signal_processor_error.interpolated_signal.magnitude)
            self.interpolated_signal_temp.append(self.signal_processor_error.interpolated_signal.magnitude)
            

            
        
        self.interpolated_signal_mag.append(self.interpolated_signal_temp)  
           
    percentage_error_function(self) 
    
    normalization(self)
 
    plot_error_map(self,self.normalized_error)
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
    #plot_error_map(self) # CALL WHEN ERROR_BUTTON IS CLICKED INSTEAD


def plot_error_map(self, data = []):
    
    self.axes.clear()
    plt.clf()
   
  

# plotting the heatmap
    erorr_map = sn.heatmap(data = data)
    
  
# displaying the plotted heatmap
    #plt.show()

    plt.title('Error Map')
    self.ErrorMap.draw()
    self.figure.canvas.draw()