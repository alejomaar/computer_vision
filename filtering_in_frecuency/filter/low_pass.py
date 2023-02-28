import numpy as np
from .fft import meshgrid

class LowPass():
    def __init__(self,rows,cols):
        self.rows: int =  rows
        self.cols: int =  cols
        
    def ideal(self,cutoff_frequency:int):
        xv,yv =meshgrid(self.rows,self.cols)
        distance_square =  xv**2 + yv**2
        return distance_square < cutoff_frequency**2
    
    def gaussian(self,cutoff_frequency:int):
        xv,yv =meshgrid(self.rows,self.cols)
        distance_square =  xv**2 + yv**2      
        return np.exp(-(distance_square)/(2*cutoff_frequency**2))
    
    def butterworth(self,cutoff_frequency:int,degree:int):
        xv,yv =meshgrid(self.rows,self.cols)
        distance =  np.sqrt(xv**2 + yv**2)        
        return 1/(1+(distance/cutoff_frequency)**(2*degree))
    
