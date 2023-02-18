import numpy as np
from filter.filter import Filter

class LowPass(Filter):
    def __init__(self,rows,cols) -> None:
        super().__init__(rows, cols)
        
    def ideal(self):
        xv,yv =self.meshgrid()
        return xv**2 + yv**2 > 150**2