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


def choices_def(self,choice):
    #max chunks is 99
    #max order is 9
    #max % is 25

    chunks=[]
    orders=[]
    overlap=[]
    if choice =="No. Of Chunks":
        for c in range (1,10):
            chunks.append(c)
        return chunks
    elif choice =="Poly. Order":
        for p in range (1,10):
            orders.append(p)
        return orders                        
    elif choice =="% Overlap":
        for p in range (1,10):
            overlap.append(p)
        return overlap
    else:
        print("DIDNOT CHOOSE ")


def select_error_x (self,x_type="No. Of Chunks"):
    self.x_type=x_type
    
    

   
    
def select_error_y (self,y_type="Poly. Order"):
    self.y_type=y_type
    self.y_values=choices_def(self,choice=self.y_type)
    

    


def calculate_error(self, loading_counter: int = 0):
    # progress bar
    # TODO: both axis should be same size
    # values  and type of axis
    # for loop to get interpolated 
    # put in array
    # compare original and interpolated
    
    self.interpolated_signal_mag=[]
  
    self.x_values=choices_def(self,choice=self.x_type)

    self.y_values=choices_def(self,choice=self.y_type)

    x=self.x_values
    y=self.y_values
    
    min_val=min(x)-1
    max_val=max(x)
    print(min_val)
    print(max_val)
    print("x_values:")
    print(self.x_values)
    
    print("x_type:")
    print(self.x_type)

    print("y_values:")
    print(self.y_values)

    print("y_type:")
    print(self.y_type)

    self.signal_processor_error=copy(self.signal_processor)
    self.signal_processor_error.interpolation_type=self.signal_processor.interpolation_type
    
    for i in x:
    # to iterate on the y ranges
        self.interpolated_signal_temp=[]
        for j in y:
        # intrapolate according to the 2 numbers and add to the matrix
            

            if ((self.y_type=="No. Of Chunks" ) and (self.x_type=="Poly. Order") ):
                self.signal_processor_error.interpolation_order=i
                self.signal_processor_error.max_chunks=j
                self.signal_processor_error.overlap_percent=self.signal_processor.overlap_percent
            elif (self.y_type=="Poly. Order" and self.x_type=="No. Of Chunks" ):
                self.signal_processor_error.interpolation_order=j
                self.signal_processor_error.max_chunks=i
                self.signal_processor_error.overlap_percent=self.signal_processor.overlap_percent
            elif (self.y_type=="No. Of Chunks" and self.x_type=="% Overlap" ):
                self.signal_processor_error.max_chunks=j
                self.signal_processor_error.overlap_percent=i
                self.signal_processor_error.interpolation_order=self.signal_processor.interpolation_order
            elif(self.y_type=="% Overlap" and self.x_type=="Poly. Order" ):
                self.signal_processor_error.interpolation_order=i
                self.signal_processor_error.overlap_percent=j
                self.signal_processor_error.max_chunks=self.signal_processor.max_chunks
            elif(self.y_type=="Poly. Order" and self.x_type=="% Overlap" ):
                self.signal_processor_error.interpolation_order=j
                self.signal_processor_error.overlap_percent=i
                self.signal_processor_error.max_chunks=self.signal_processor.max_chunks
            elif(self.y_type=="% Overlap" and self.x_type=="No. Of Chunks" ):
                self.signal_processor_error.max_chunks=i
                self.signal_processor_error.overlap_percent=j
            else:
                print("seriously 3adat kol dah!!")
             
            print("x=")
            print(i)
            print("y=")
            print(j)
            self.signal_processor_error.interpolate() 
            self.interpolated_signal_temp.append(self.signal_processor_error.interpolated_signal.magnitude)
            

            
        
        self.interpolated_signal_mag.append(self.interpolated_signal_temp)  
    print("magitudes in 2d:")
    print(self.interpolated_signal_mag)       
         
    # percentage_error between interpolated signal and original signal
    self.percentage_error=[]
    
    for i in range(min_val,max_val):
        self.percentage_error_temp=[]
        for j in range(min_val,max_val):
            clipped_signal_avg=np.average(self.signal_processor_error.clipped_signal.magnitude)
            interpolated_signal_avg=np.average(self.interpolated_signal_mag[i][j])
            self.percentage_error_temp.append((np.absolute(interpolated_signal_avg-clipped_signal_avg / clipped_signal_avg )))
        self.percentage_error.append(self.percentage_error_temp)
        print("there")
    print("percentage_error:")
    print(self.percentage_error)
    

    self.normalized_error=[]
    
    for i in range(min_val,max_val):
        self.normalized_error_temp=[]
        for j in range(min_val,max_val):
            value=(self.percentage_error[i][j] - np.amin(self.percentage_error)) / (np.amax(self.percentage_error) - np.amin(self.percentage_error))
            self.normalized_error_temp.append(value)
        self.normalized_error.append(self.normalized_error_temp)
        print("NORM")
    print("NORMALIZED:")
    print(self.normalized_error)

   
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
    calculate_error(self)
    self.axes.clear()
     
    data = self.normalized_error
  

# plotting the heatmap
    erorr_map = sn.heatmap(data = data)
    
  
# displaying the plotted heatmap
    #plt.show()

    plt.title('Error Map')
    self.ErrorMap.draw()
    self.figure.canvas.draw()