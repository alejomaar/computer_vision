# @author: Manuel Alejandro Aponte
# Program to find difference between two images


import cv2
import numpy as np

top_left_corner=[]
bottom_right_corner=[]

# Load image
image = cv2.imread('hallway.jpg')
image = cv2.resize(image, (400,600))


def drawRectangle(action, x, y, flags, *userdata):
      # Referencing global variables 
  global top_left_corner, bottom_right_corner
  
  print(x,y,action)
  # Mark the top left corner when left mouse button is pressed
  if action == cv2.EVENT_LBUTTONDOWN:
    top_left_corner = [(x,y)]
    # When left mouse button is released, mark bottom right corner
  elif action == cv2.EVENT_LBUTTONUP:
    bottom_right_corner = [(x,y)]    
    # Draw the rectangle
    cv2.rectangle(image, top_left_corner[0], bottom_right_corner[0], (0,255,0),2, 8)
    #cv2.imshow("window",image)

    
cv2.namedWindow("window")
cv2.setMouseCallback("window", drawRectangle,image)


#transform = np.array([[1,0,0],[1,0,0],[1,0,0]])
#img_transform = cv2.warpPerspective(img, transform)


while True:
    # both windows are displaying the same img
    cv2.imshow("window", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()