import numpy as np

class Filter:
    def __init__(self,rows,cols) -> None:
        self.rows = rows
        self.cols = cols
        
    def meshgrid(self):
        """
        Create a mesh grid of coordinates centered around the center.

        Returns
        -------
        xv, yv : 2D arrays
            Arrays containing the x and y coordinates of the mesh grid.

        """
        center_row = int(self.rows/2)
        center_cols = int(self.cols/2)
        
        x = np.linspace(0, self.cols, self.cols)- center_cols
        y = np.linspace(0, self.rows, self.rows) -center_row
        xv, yv = np.meshgrid(x, y)
        return xv, yv