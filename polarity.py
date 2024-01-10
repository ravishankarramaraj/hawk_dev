# import cv2
# import numpy as np
# import os
# img_rgb = cv2.imread('D:/Camera/cropped1.png')
# img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# # Read the template 
# template = cv2.imread('D:/Camera/c2.png', 0) 
  
# # Store width and height of template in w and h 
# w, h = template.shape[::-1] 
  
# # Perform match operations. 
# res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED) 
  
# # Specify a threshold 
# threshold = 0.8
  
# # Store the coordinates of matched area in a numpy array 
# loc = np.where(res >= threshold) 
  
# # Draw a rectangle around the matched region. 
# for pt in zip(*loc[::-1]): 
#     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2) 
  
# # Show the final image with the matched area. 
# img_rgb = cv2.resize(img_rgb, (640, 480))
# cv2.imshow('Detected', img_rgb)
# cv2.waitKey(0) 

import cv2 
import numpy as np 
from imutils.object_detection import non_max_suppression 

# Reading the image and the template 
img = cv2.imread('D:/Camera/cropped1.png') 
temp = cv2.imread('D:/Camera/c2_1.png') 

# save the image dimensions 
W, H = temp.shape[:2] 

# Define a minimum threshold 
thresh = 0.5

# Converting them to grayscale 
img_gray = cv2.cvtColor(img, 
						cv2.COLOR_BGR2RGB) 
temp_gray = cv2.cvtColor(temp, 
						cv2.COLOR_BGR2RGB) 

# Passing the image to matchTemplate method 
match = cv2.matchTemplate( 
	image=img_gray, templ=temp_gray, 
method=cv2.TM_CCOEFF_NORMED) 

# Select rectangles with 
# confidence greater than threshold 
(y_points, x_points) = np.where(match >= thresh) 

# initialize our list of rectangles 
boxes = list() 

# loop over the starting (x, y)-coordinates again 
for (x, y) in zip(x_points, y_points): 
	
	# update our list of rectangles 
	boxes.append((x, y, x + W, y + H)) 

# apply non-maxima suppression to the rectangles 
# this will create a single bounding box 
boxes = non_max_suppression(np.array(boxes)) 

# loop over the final bounding boxes 
for (x1, y1, x2, y2) in boxes: 
	
	# draw the bounding box on the image 
	cv2.rectangle(img, (x1, y1), (x2, y2), 
				(255, 0, 0), 3) 
img = cv2.resize(img, (640, 480))
# Show the template and the final output 
cv2.imshow("Template", temp) 
cv2.imshow("After NMS", img) 
cv2.waitKey(0) 

# destroy all the windows 
# manually to be on the safe side 
cv2.destroyAllWindows() 
