import numpy as np
from filter.filter import Filter

class HighPass(Filter):
    def __init__(self,rows,cols) -> None:
        super().__init__(rows, cols)
        
    def ideal(self,cutoff_frequency:int):
        xv,yv =self.meshgrid()
        return xv**2 + yv**2 < cutoff_frequency**2
    
    def gaussian(self,cutoff_frequency:int):
        xv,yv =self.meshgrid()        
        return 1-np.exp(-(xv**2 + yv**2)/(2*cutoff_frequency**2))