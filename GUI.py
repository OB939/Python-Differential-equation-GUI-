# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 18:52:49 2019

@author: ZFAP036
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 14:51:09 2019

@author: ZFAP036
"""

#Imports neccessary modules 
import sys
import PyQt5.QtWidgets as Qt
import numpy as np
import os 

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy,QPushButton, QAction, QLineEdit, QMessageBox,QTabWidget,QMainWindow,QToolTip

# Load the matplotlib backend tools
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar


from matplotlib.figure import Figure
#Here we generate a class which generates our canvas figure 
class MPLCanvas(FigureCanvas): #The class inherits from the FigureCanvas module 
    def __init__(self, type="2d"): #In our constructor we define our figure which we shall later add things too.
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setupPlotAx(type='2d') #Here we are adding two subplots to our canvas, we are setting our plots to be 2D
        self.setupPlotAx2(type='2d')
    def setupPlotAx(self, type):
        self.ax = self.fig.add_subplot(121) #We are defining a variable self.ax and adding it to our subplot 
    def setupPlotAx2(self, type):
        self.ax2 = self.fig.add_subplot(122)
        
        
class MatPlotLibWidget(QWidget): #In this class we are creating a set of widgets that we will add to the canvas, our class inherits from the QWidget module 
    def __init__(self, parent, type="2d"):
        QWidget.__init__(self, parent)

        self.canvas = MPLCanvas(type)
        self.toolbar = NavBar(self.canvas, self)
        self.ax = self.canvas.ax
        self.ax2 = self.canvas.ax2

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
    def clearCanvas(self):
        self.canvas.ax.clear()
        self.canvas.ax2.clear()

    def update(self):
        self.canvas.draw()

class MyTableWidget(QWidget):#This class generates a table widget 
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self) #Sets the layout of the tab 
        
        self.tabs = QTabWidget() #Uses the tab widget 
        self.tab1 = QWidget() #Defines a variable self.tab1 which is equal to a Qwidget 
        self.tab2 = QWidget()
        self.tabs.resize(200,100) #Sets the dimensions of the tabs
        tab1vbox=QVBoxLayout(self)
        tab2vbox=QVBoxLayout(self)
        self.tab1.setLayout(tab1vbox)#Defines the layout of the first tab 
        self.tab2.setLayout(tab2vbox)
        self.tabs.setToolTip("Learn about the different methods")
        self.tabs.addTab(self.tab1,"Euler Method") #Adds our tab 1 variable to the Tab widget 
        self.tabs.addTab(self.tab2,"Runge-Kutta Method")
        #Bellow we create two variables which are equal to some string of text.
        text1=Qt.QTextEdit("The Euler Method for solving differential equations involves iterating over a finite number of small segments dx. In the case of the damped oscillator we iterate over a finte number of segments dt over the time period over which we wish to measure the oscilators motion. For each time element we calculate the angular acceleration at that instance and the current angular displacement by using the value of the angular velocity from the previous time segment dt, thus we are able to plot the angular displacement of the pendulum as a function of time. A source of inaccuarcy arises from the fact that each position is calculated using the previous value of angular velcoity, for the case of a damped oscillator this results in our euler method diverging from the real solution.   ")
        text2=Qt.QTextEdit("The Runge-Kutta method is a vastly superior method of approximating the solutions of differential equations, though it follows the same basic proceedure as the Euler formula it uses a more sophisticated method to compute the average of a slope over a time interval. That is, we compute the corresponding values of angular displacement, velocity and acceleration at certain intances within the time interval and then take the average of these instances. Ultimately this yields a more accuarate solution to the differential equation, which in this instance models the motion of a damped oscilator.")
        text1.setReadOnly(True) #Prevents the user from editing the text in the GUI 
        text2.setReadOnly(True)
        reportbtn=QPushButton("View report") #Defines a variable which is equal to a pushbutton which opens the report 
        reportbtn.clicked.connect(self.open_report) 
        reportbtn.setToolTip("Open report on GUI")
        
        
        self.layout.addWidget(self.tabs) #Adds the tab to the layout of the widget
        self.setLayout(self.layout)
        tab1vbox.addWidget(text1) #Adds text to the layout of the tabs. 
        tab2vbox.addWidget(text2)
        tab1vbox.addWidget(reportbtn)
        
    def open_report(self):
        os.startfile("PH114_Sample.pdf")    
    def on_click(self): #This method means that the contents of the tab is displayed when clicked on by the user. 
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
class LabeledInput(Qt.QWidget): #This class creates the labelled inputs. 
    def __init__(self, parent, label, inputType=Qt.QDoubleSpinBox):
       
        Qt.QWidget.__init__(self, parent)

        hLayout = Qt.QHBoxLayout() #Creates the layout of the labels 
        label = Qt.QLabel(label) #Sets a variable label equal to the label widget imported from Qt 
        self.input = inputType()        
        hLayout.addWidget(label) #Adds the label variable to the layout 
        hLayout.addWidget(self.input)
        self.setLayout(hLayout)
        self.setToolTip("Adjust your parameters and inital conditions") #Generates a tool tip which displays the text enclosed in the brackets 
    
    def setValue(self, value):
        return self.input.setValue(value)
    
    def value(self):
        return self.input.value()
   
        
class PlotPen(Qt.QWidget): #This class generates the GUI 
    def __init__(self):
        Qt.QWidget.__init__(self)

        self.aVal = LabeledInput(self, "Inital angular velocity") #Uses previously defined label widget to generate a series of user input tabs corresponding to the variables in the ODE
        self.bVal = LabeledInput(self, "Inital angular displacement")
        self.cVal = LabeledInput(self, "Damping")
        self.dVal = LabeledInput(self, "Length of pendulum")
        self.g=9.81
        self.t=0.0
        self.tf=20.0
        self.dt=0.05
        self.t2=0.0
        self.vlist=[]  #Creates a set of empty lists to be used later in functions 
        self.t2list=[] 
        self.x2list=[]
        self.aVal.setValue(1) #Sets the inital values of the variables in the ODE
        self.bVal.setValue(0)
        self.cVal.setValue(0.5)
        self.dVal.setValue(2)
        
        self.plotBtn = QPushButton("Plot motion") #Creates a pushbutton which will plot the graphs 
        self.plotBtn.setToolTip("Click here to plot graphs")

        vLayout= Qt.QVBoxLayout() 
        self.setLayout(vLayout)

        hLayout = Qt.QHBoxLayout()                
        hLayout.addWidget(self.aVal) #Adds our labeled inputs to the layout.
        hLayout.addWidget(self.bVal)
        hLayout.addWidget(self.cVal)
        hLayout.addWidget(self.dVal)
        
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.plotBtn)
     
        self.addPlotCanvas(vLayout)

        self.plotBtn.clicked.connect(self.replot)#This allows our graphs to replot when the parameters are adjusted 
    def addPlotCanvas(self, vLayout):#This method generates a method to which 
        self.plotCanvas = MatPlotLibWidget(self, type=str(int(self.dVal.value()))+"d")
        vLayout.addWidget(self.plotCanvas) #Here we are adding our window to the final class 
        self.table_widget = MyTableWidget(self)
        vLayout.addWidget(self.table_widget) #Here we are adding out user defined tab widget to the final class.
    def displacement(self,v0,r0,B,l): #This method creates the Euler function approximation of the ODE
        self.t=0 #Sets some initial parameters which the method will operate in 
        self.tlist=[] #And empty list which the while loop will append values to.
        self.xlist=[]
        while self.t<self.tf: #This generates a while loop which is only executed when our value for time is less than tf.
            a=(-B*v0)-(np.sin(r0))*(np.sqrt(self.g/l)**2)#Acceleration from previous time step 
            r0=r0+v0*self.dt #Displacement for time step
            v0=v0+a*self.dt #Velocity for time step 
            self.t=self.t+self.dt #Increases the value of time by adding the duration of the time step to our time variable.
            self.tlist.append(self.t) #Appends our value of time to the list.
            self.xlist.append(r0)#Appends our value for position to the list. 
        return self.tlist,self.xlist #  Outside the loop the method returns the updated lists 
    def Runge_Kutta(self,v0,r0,B,l): #Creates the Runge_kutta method 
        k1r=(v0*self.dt) #Defines a new varialbe k1r which is equal to the angular dispplacement differential 
        k1v=(-B*v0-np.sin(r0+k1r)*(np.sqrt(self.g/l))**2)*self.dt #Defines a new variable k1v which is equal to the angular velcoity differential 
        k2r=self.dt*(v0+k1v+k1r/2)
        k2v=(-B*(v0+k1v/2)-np.sin(r0+k2r)*(np.sqrt(self.g/l))**2)*self.dt
        k3r=self.dt*(v0+k2v+k2r/2)
        k3v=(-B*(v0+k2v/2)-np.sin(r0+k3r)*(np.sqrt(self.g/l))**2)*self.dt
        k4r=self.dt*(v0+k3v+k3r/2)
        k4v=(-B*(v0+k3v/2)-np.sin(r0+k4r)*(np.sqrt(self.g/l))**2)*self.dt
        
        r=r0+(k1r+2*(k2r+k3r)+k4r)/6 #Calculates the position of the pendulum after the time step.
        v=v0+(k1v+2*(k2v+k3v)+k4v)/6 #Calculates the velcoity of the pendulum after the time step.
        
        return r,v #Returns these new values. 
      
    def replot(self):
        # Get the values in the boxes
        self.plotCanvas.clearCanvas()
        a = self.aVal.value() #Sets our input boxes equal to a set of parameters. 
        b = self.bVal.value()
        c = self.cVal.value()
        d = self.dVal.value()
      
        t,r=self.displacement(a,b,c,d) #Calls our euler function with the paramtets from the input boxes substituted.
        self.t2list.append(self.t2) 
        self.x2list.append(b)
        while self.t2<self.tf: #Generates a wile loop for our Runge-Kutta function 
           b,a=self.Runge_Kutta(a,b,c,d) #Updates values of angular displacement and angular velocity.
           self.x2list.append(b) #Appends updated value of angular displacement to the list 
           self.t2=self.t2+self.dt #Updates value of time 
           self.t2list.append(self.t2) #Appends updated time value to list. 
        self.plotCanvas.ax.plot(t, r) #Plots our Euler method 
        self.plotCanvas.ax.set_title("Euler method")
        self.plotCanvas.ax.set_xlabel("Time (Seconds)")
        self.plotCanvas.ax.set_ylabel("Angular displacement (Radians)")
        self.plotCanvas.ax2.plot(self.t2list,self.x2list) #Plots runge kutta method 
        self.plotCanvas.ax2.set_title("Runge-Kutta method")
        self.plotCanvas.ax2.set_xlabel("Time(Seconds)")
        self.plotCanvas.ax2.set_ylabel("Angular displacement (Radians)")
        self.plotCanvas.canvas.draw()
        self.x2list=[] #Resets values for runge-kutta method if the programme is run again by the user.
        self.t2list=[]
        self.t2=0
        



app = Qt.QApplication(sys.argv)
w=PlotPen()
w.show()
exit(app.exec_())