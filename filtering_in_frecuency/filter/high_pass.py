import numpy as np
from filter.filter import Filter

class HighPass(Filter):
    def __init__(self,rows,cols) -> None:
        super().__init__(rows, cols)
        
    def ideal(self,cutoff_frequency:int):
        xv,yv =self.meshgrid()
        distance_square =  xv**2 + yv**2 
        return distance_square < cutoff_frequency**2
    
    def gaussian(self,cutoff_frequency:int):
        xv,yv =self.meshgrid()
        distance_square =  xv**2 + yv**2         
        return 1-np.exp(-(distance_square)/(2*cutoff_frequency**2))
    
    def butterworth(self,cutoff_frequency:int):
        xv,yv =self.meshgrid() 
        distance =  np.sqrt(xv**2 + yv**2)        
        return 1-1/(1+(distance/cutoff_frequency)**4)