import sys, re,LinearFIR, threshold, linear, improbability, spectral_pattern, webbrowser, os
from numpy import *
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox, QVBoxLayout, QAbstractItemView,
                             QTableWidgetItem, QComboBox)
from PyQt5.uic import loadUi;
from PyQt5 import QtGui,QtCore, QtWidgets;
from scipy.signal import welch
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class lanzarApp(QMainWindow):  
    def __init__(self):       
        
        QMainWindow.__init__(self);
        loadUi('welcome_window.ui',self);
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        
        self.field_fileName.setDisabled(True)
        self.in_Fs.setDisabled(True)
        self.button_graph.setDisabled(True)
        self.button_graphfilter.setDisabled(True)
        self.button_threshold.setDisabled(True)
        self.button_linear.setDisabled(True)
        self.button_kurtosis.setDisabled(True)
        self.button_spectrum.setDisabled(True)
        
        self.button_file.clicked.connect(self.getfile);
        self.button_file.setToolTip('Seleccionar archivo de texto de señal EEG')
        self.in_Fs.textChanged.connect(self.Fs_changed)
        self.button_graph.clicked.connect(self.graph_signal);
        self.button_graphfilter.clicked.connect(self.graph_filter);
        self.button_threshold.clicked.connect(self.threshold_method);
        self.button_threshold.setToolTip('Eliminación de artefactos por el método del umbral')
        self.button_linear.clicked.connect(self.linearTrend_method);
        self.button_linear.setToolTip('Eliminación de artefactos por el método de tendencias lineales')
        self.button_kurtosis.clicked.connect(self.improbability_method);
        self.button_kurtosis.setToolTip('Eliminación de artefactos por el método de improbabilidad')
        self.button_spectrum.clicked.connect(self.spectral_method);
        self.button_spectrum.setToolTip('Eliminación de artefactos por el método de gráfico espectral')
        self.button_guide.clicked.connect(self.open_userguide)
        self.button_guide.setToolTip('Abrir el manual de usuario de la aplicación')
        
    def open_userguide(self):
        path=(os.path.dirname(sys.argv[0]))+'\Manual.pdf'
        webbrowser.open(path)
    
    def getfile(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Text files (*.txt )")
        self.field_fileName.setText(self.fname[0])
        
        if self.field_fileName.text()!='':
            self.in_Fs.setDisabled(False)
            
    def fileName(self):
        name=self.field_fileName.text()
       
         
        self.file=loadtxt(name,delimiter = ',',skiprows = 6,dtype = bytes,usecols = arange(1,9)).astype(str)
        self.file = self.file.transpose()
        self.file = self.file.astype(float)
        
        return(self.file)
            
    def Fs_changed(self):
        self.validate_Fs()
        if self.validate_Fs():
            self.button_graph.setDisabled(False)
            self.button_graphfilter.setDisabled(False)
            self.button_threshold.setDisabled(False)
            self.button_linear.setDisabled(False)
            self.button_kurtosis.setDisabled(False)
            self.button_spectrum.setDisabled(False)
            self.label_selectMethod.setText('Seleccione alguno de los métodos para eliminación de artefactos') 
            Fs=int(self.in_Fs.text())
            
            return Fs
        else:
            self.button_graph.setDisabled(True)
            self.button_graphfilter.setDisabled(True)  
            self.button_threshold.setDisabled(True)
            self.button_linear.setDisabled(True)
            self.button_kurtosis.setDisabled(True)
            self.button_spectrum.setDisabled(True)    
            self.label_selectMethod.setText('')      
        
        
    def validate_Fs(self):
        self.Fs = self.in_Fs.text();
        validate_Fs = re.match('^[0-9]{1,5}$', self.Fs)
        if self.Fs=='' : 
            self.in_Fs.setStyleSheet("border:2px solid yellow;")
            self.label_warningFs.setText("Este campo es obligatorio")
            return False
        elif not validate_Fs:
            self.in_Fs.setStyleSheet("border: 2px solid red;")
            self.label_warningFs.setText("Digite caracteres válidos")
            return False
        else:
            self.in_Fs.setStyleSheet("border: 2px solid green;")
            self.label_warningFs.setText("")
            return True
        
    def graph_signal(self):
        data=self.fileName()
        Fs=self.Fs_changed()
        self.graph_window = window_graph(data, Fs,1);
        self.graph_window.show();
        
    def filter_signal(self):
        data=self.fileName()
        Fs=self.Fs_changed()
        
        self.signal2filter=data
        self.filteredChannels=ndarray(shape = shape(self.signal2filter), dtype = self.signal2filter.dtype)
        channels, points = self.signal2filter.shape
        self.time_array=arange(0,points/Fs,1/Fs)
        
        for i in range(channels):
            highpass_signal=LinearFIR.eegfiltnew(self.signal2filter[i,::], Fs, locutoff=1, hicutoff=0, revfilt=0, plot=0)
            lowpass_signal=LinearFIR.eegfiltnew(highpass_signal, Fs, locutoff=0, hicutoff=50, revfilt=0, plot=0)
            self.filteredChannels[i,::]=lowpass_signal

        return self.filteredChannels
    
    def graph_filter(self):
        Fs=self.Fs_changed()
        self.data=self.filter_signal()
        self.graph_window = window_graph(self.data, Fs,2);
        self.graph_window.show();
        
        
    def threshold_method(self):

        data=self.filter_signal()
        Fs=self.Fs_changed()
        self.threshold_window = method_window(data,Fs);
        self.threshold_window.show();
        
    def linearTrend_method(self):
        data=self.filter_signal()
        Fs=self.Fs_changed()
        self.linearTrend_window = methods_window(data,Fs,1);
        self.linearTrend_window.show();
        
    def improbability_method(self):
        data=self.filter_signal()
        Fs=self.Fs_changed()
        self.improbability_window = methods_window(data,Fs,2);
        self.improbability_window.show();
    
    def spectral_method(self):
        data=self.filter_signal()
        Fs=self.Fs_changed()
        frecs,pots=self.welch_data(data,Fs)
        self.spectral_window = spectralPattern_window(pots,frecs,data,Fs);
        self.spectral_window.show();
#         self.linearTrend_window = methods_window(data,Fs,3);
#         self.linearTrend_window.show();
        
    def welch_data(self,data,Fs):
        pots=zeros(shape=(shape(data)[0],(int((shape(data)[1])/2))+1))
        frecs=zeros(shape=(shape(data)[0],(int((shape(data)[1])/2))+1))
   
        for i in range(shape(data)[0]):
            x=data[i,::]
       
            frec,pxx=welch(x,Fs,nperseg=len(x))
                   
       
            pots[i,:]=pxx
            frecs[i,:]=frec
        return frecs,pots
            
        
        
        
class window_graph(QDialog):
    def __init__(self,data,Fs,status,methodValues=0,deletedEpochs=0,totalepochs=0):         
        QDialog.__init__(self);
        loadUi('graph.ui',self);
        self.setWindowIcon(QtGui.QIcon("logo.png"))
                
        self.mySignal=data
        self.myFs=Fs
        self.status=status
        self.methodSignal=methodValues
        self.deletedEpochs=deletedEpochs
        self.numEpochs=totalepochs
        
        self.channels, self.points = shape(self.mySignal)
        #self.time_array=arange(0,self.points/self.myFs,1/self.myFs)
        
        self.button_zoom.clicked.connect(self.zoom)
        self.button_pan.clicked.connect(self.pan)
        self.button_home.clicked.connect(self.home)
        
        self.figure = Figure(figsize=(5,4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.axes=self.figure.add_subplot(111)
        self.toolbar=NavigationToolbar(self.canvas,self)
        self.toolbar.hide()
        
        layout=QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.field_graph.setLayout(layout)
        self.axes.clear()
        self.canvas.draw()
        self.plot()
        
    def plot(self):
        legends=['Ch 1','Ch 2','Ch 3','Ch 4','Ch 5','Ch 6','Ch 7','Ch 8']
        if self.status==1:
            for c in range(self.channels):
                self.axes.plot(self.mySignal[c,::])
            self.axes.legend(legends)   
            self.axes.set_title('Señal original')
        if self.status==2:
            r=[]
            for c in range(self.channels):
                r.append(c*150)
                self.axes.plot(self.mySignal[c,::]+c*150)
            self.axes.set_yticklabels(legends)
            self.axes.set_yticks(r)
            self.axes.set_title('Señal filtrada')
            
        if self.status==3:
            r=[]
            for c in range(self.channels):
                r.append(c*150)
                self.axes.plot(self.mySignal[c,::]+c*150)
                self.axes.plot(self.methodSignal[c,::]+c*150,'r')
                
            self.axes.set_yticklabels(legends)
            self.axes.set_yticks(r)   
            self.axes.set_title('Eliminación de épocas') 
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Se eliminaron las épocas : "+'  '.join(str(ep) for ep in self.deletedEpochs))
            msg.setWindowTitle("Épocas eliminadas")
            msg.setInformativeText("Épocas iniciales: "+str(self.numEpochs)+'\tÉpocas restantes: '+str(self.numEpochs-len(self.deletedEpochs)))
            msg.show();

            
        self.axes.set_ylabel('Voltaje [uV]') 
        self.axes.set_xlabel('Muestras')  
        self.axes.grid(True)
        self.axes.set_xlim([0,4000])
        


        self.canvas.draw()
 
    def home(self):
        self.toolbar.home()
    def zoom(self):
        self.toolbar.zoom()
    def pan(self):
        self.toolbar.pan()
        
class method_window(QDialog):
    def __init__(self,data,Fs):         
        QDialog.__init__(self);
        loadUi('method_threshold.ui',self);
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.data=data
        self.Fs=Fs
        self.channels,self.points=shape(self.data)
        self.epochs(self.data, self.channels, self.points)
        
        self.button_apply.clicked.connect(self.implementation)
        self.button_cancel.clicked.connect(self.cancelar)
        self.label_title.setText('Eliminación de artefactos por superación de umbral')
        
    def cancelar(self):
        method_window.close(self);  
    
    def epochs(self,data,channels,points):
        self.filtered_signal=data
        self.size_epoch=self.Fs*2
        self.num_epoch=points/self.size_epoch
        delete=points%self.size_epoch
         
        self.filtered_signal=self.filtered_signal[::,0:(points-delete)]
        self.epochs_file=reshape(self.filtered_signal,(channels,int(self.size_epoch),int((points-delete)/self.size_epoch)),order='F')
        return(self.epochs_file)
    
    def implementation(self):
        min_value=float(self.field_minValue.text())
        
        max_value=float(self.field_maxValue.text())
        self.myepochs=self.epochs(self.data, self.channels, self.points)
        

        x,y=threshold.threshold(self.myepochs, min_value, max_value)
        
        newSignal=reshape(x,(shape(x)[0],shape(x)[1]*shape(x)[2]),order='F')
        
        self.graph_method = window_graph(self.data, self.Fs,3,newSignal,y,shape(self.myepochs)[2]);
        
        self.graph_method.show();
        
class methods_window(QDialog):
    def __init__(self,data,Fs,status):         
        QDialog.__init__(self);
        loadUi('method.ui',self);
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.data=data
        self.Fs=Fs
        self.status=status
        self.channels,self.points=shape(self.data)
        self.epochs(self.data, self.channels, self.points)
        
        self.button_apply.clicked.connect(self.implementation)
        self.button_cancel.clicked.connect(self.cancelar)
        
        
        if self.status==1:
            self.label_title.setText('Eliminación de artefactos por tendencias lineales')
            self.label_maxValue.setText('Valor máximo [pendiente]')
        if self.status==2:
            self.label_title.setText('Eliminación de artefactos por improbabilidad')
            self.label_maxValue.setText('Valor máximo [kurtosis]')
        if self.status==3:
            self.label_title.setText('Eliminación de artefactos por espectro de potencia')
            self.label_maxValue.setText('Valor máximo [potencia]')
     
    def cancelar(self):
        methods_window.close(self);    
        
    def epochs(self,data,channels,points):
        self.filtered_signal=data
        self.size_epoch=self.Fs*2
        self.num_epoch=points/self.size_epoch
        delete=points%self.size_epoch
         
        self.filtered_signal=self.filtered_signal[::,0:(points-delete)]
        self.epochs_file=reshape(self.filtered_signal,(channels,int(self.size_epoch),int((points-delete)/self.size_epoch)),order='F')
        return(self.epochs_file)
    
    def implementation(self):
        
        max_value=float(self.field_maxValue.text())
        self.myepochs=self.epochs(self.data, self.channels, self.points)
        
        if self.status==1:
            x,y=linear.linearTrends(self.myepochs, max_value)
        if self.status==2:
            x,y=improbability.kurt(self.myepochs, max_value)
        
        newSignal=reshape(x,(shape(x)[0],shape(x)[1]*shape(x)[2]),order='F')
        self.graph_method = window_graph(self.data, self.Fs,3,newSignal,y,shape(self.myepochs)[2]);
        self.graph_method.show();
        
        
class spectralPattern_window(QDialog):
    def __init__(self,pxx,frequencies,data,Fs):         
        QDialog.__init__(self);
        loadUi('graph_spectral.ui',self);
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.label_title.setText('Eliminación de artefactos por espectro de potencia')
        self.label_maxValue.setText('Valor máximo [potencia]')
        
        self.data=data
        self.Fs=Fs
        self.channels,self.points=shape(self.data)
        self.epochs(self.data, self.channels, self.points)
        self.pxx=pxx
        self.frequencies=frequencies
        
        
            
        
        self.button_zoom.clicked.connect(self.zoom)
        self.button_pan.clicked.connect(self.pan)
        self.button_home.clicked.connect(self.home)
        self.button_apply.clicked.connect(self.implementation)
        self.button_cancel.clicked.connect(self.cancelar)
        self.figure = Figure(figsize=(5,4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.axes=self.figure.add_subplot(111)
        self.toolbar=NavigationToolbar(self.canvas,self)
        self.toolbar.hide()
         
        layout=QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.field_graph.setLayout(layout)
        self.axes.clear()
        self.canvas.draw()
        self.plot()
        
    def cancelar(self):
        spectralPattern_window.close(self);
        
    def home(self):
        self.toolbar.home()
    def zoom(self):
        self.toolbar.zoom()
    def pan(self):
        self.toolbar.pan()
         
    def plot(self):
        legends=['Ch 1','Ch 2','Ch 3','Ch 4','Ch 5','Ch 6','Ch 7','Ch 8']
        r=[]
        
        for c in range(shape(self.pxx)[0]):
            r.append(c*35)
            self.axes.plot(self.frequencies[c,::],sqrt(self.pxx[c,::])+c*35,linewidth=0.5)
        self.axes.set_yticklabels(legends)
        self.axes.set_yticks(r)
        self.axes.grid(True)
        self.axes.set_xlim([0,40])
        self.axes.set_xlabel('Frecuency [Hz]')
        self.axes.set_ylabel('Power density [V^2/Hz]')
        self.axes.set_title('Periodograma de Welch') 
        
    def epochs(self,data,channels,points):
      
        self.filtered_signal=data
        
        self.size_epoch=self.Fs*2
        self.num_epoch=points/self.size_epoch
        delete=points%self.size_epoch
          
        self.filtered_signal=self.filtered_signal[::,0:(points-delete)]
        self.epochs_file=reshape(self.filtered_signal,(channels,int(self.size_epoch),int((points-delete)/self.size_epoch)),order='F')
        return(self.epochs_file)
#         
    def implementation(self):
        max_value=float(self.field_maxValue.text())
        self.myepochs=self.epochs(self.data, self.channels, self.points)
        x,y=spectral_pattern.spectral(self.myepochs, max_value,self.Fs)
        newSignal=reshape(x,(shape(x)[0],shape(x)[1]*shape(x)[2]),order='F')
        self.graph_method = window_graph(self.data, self.Fs,3,newSignal,y,shape(self.myepochs)[2]);
        self.graph_method.show();

        
        
        
        
app = QApplication(sys.argv)
widget = lanzarApp()  
widget.show()
sys.exit(app.exec_())