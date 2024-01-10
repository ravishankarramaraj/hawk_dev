# import cv2
# import numpy as np
# import os

# folder = 'D:/Camera/111223_lightingimages'#'D:/CV_Inspection/Hawk/HBLpcbs'

# framecounter = 0
# for filename in os.listdir(folder):
#     framecounter += 1
#     i = 0
#     img = cv2.imread(os.path.join(folder,filename))
#     y=1878
#     x=595
#     h=1727
#     w=2829
#     crop = img[y:y+h, x:x+w]
#     cv2.imshow('Image', crop)
#     cv2.waitKey(0) 

from PIL import Image
 
# Load the image
im = Image.open('D:/Camera/cropped1.png')
 
width, height = im.size
dpi = im.info.get("dpi", (144, 144))
print(dpi[0])
Pixel_per_cm = dpi[0] / 2.54
width_cm = width / Pixel_per_cm
height_cm = height / Pixel_per_cm

centi = width_cm
y = 38.431
pixels = ( dpi[0] * centi) / 2.54
print ( round(pixels, 2)) 

print("Image Width : ", width)
print("Image Height : ", height)
print("Width in cm", width_cm)
print("Height in cm", height_cm)

Focal_length = 16 #mm
Sensor_width_pixels = 5472
Sensor_width_mms = 13.13
Sensor_length_pixels = 3648
Sensor_length_mms = 8.76
Object_length_meters = 0.14
Object_width_meters = 0.215
distance = 0.77 #Meters

Object_width_on_sensor_mms=(Focal_length*Object_width_meters)/distance
    #Object_width_on_sensor_mms2
Object_width_pixels=(Sensor_width_pixels*Object_width_on_sensor_mms)/Sensor_width_mms
Object_length_on_sensor_mms=(Focal_length*Object_length_meters)/distance
Object_length_pixels=(Sensor_length_pixels*Object_length_on_sensor_mms)/Sensor_length_mms
#print(f'Object_actual_size={Object_length_meters} x {Object_width_meters}(meters) at {distance}(meters) distance coresponds to Object_pixel_size={Object_length_pixels} x {Object_width_pixels}(pixels)')
print("Object size in Pixels ", Object_width_pixels,Object_length_pixels)   
#Object_width_pixels = 2570
#Object_length_pixels = 1686

Object_width_on_sensor_mms=(Sensor_width_mms*Object_width_pixels)/Sensor_width_pixels    
Object_width_meters=((distance*Object_width_on_sensor_mms)/Focal_length)
Object_length_on_sensor_mms=(Sensor_length_mms*Object_length_pixels)/Sensor_length_pixels
Object_length_meters=((distance*Object_length_on_sensor_mms)/Focal_length)

#print(f'Object_pixel_size={Object_length_pixels} x {Object_width_pixels}(pixels) at {distance}(meters) distance corresponds to Object_actual_size={Object_length_meters} x {Object_width_meters}(meters)')
print("Object size in Meters ",(Object_width_meters*100),(Object_length_meters*100))