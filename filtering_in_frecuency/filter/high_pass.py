import numpy as np
from filter.filter import Filter

class HighPass(Filter):
    def __init__(self,rows,cols) -> None:
        super().__init__(rows, cols)
        
    def ideal(self,threshold):
        xv,yv =self.meshgrid()
        return xv**2 + yv**2 < threshold**2