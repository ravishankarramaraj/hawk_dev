import cv2
import numpy as np
from pypylon import pylon
from datetime import datetime
import neoapi
import time

camera = neoapi.Cam()
camera.Connect()
imagecnt = 0
if camera.IsConnected():
    camera.f.PixelFormat.SetString('BGR8')
    f = camera.f.LineSelector
    f.value = neoapi.LineSelector_Line0                                                    
    camera.f.ExposureTime.Set(1500)
    camera.f.TriggerMode.value = neoapi.TriggerMode_On  # set camera to trigger mode
    camera.f.TriggerSource.value = neoapi.TriggerSource_Line0
    camera.f.TriggerActivation.value = neoapi.TriggerActivation_RisingEdge
    camera.f.TriggerDelay.value = 350000.000000        #nailpolish: 25, only Denver:33
    camera.f.Gain.value = 10.84
    camera.f.OffsetX = 1200
    camera.f.OffsetY = 712
    camera.f.Width = 1456
    camera.f.Height = 1464
    while camera.IsOnline():
        for i in range(1000):
            imagecnt +=1
            inputimg = camera.GetImage(1000000).GetNPArray()
            new_width = 1080 
            ratio = new_width / 1456
            new_height = int(1464 * ratio)
            dimensions = (new_width, new_height)
            inputimg = cv2.resize(inputimg, dimensions, interpolation=cv2.INTER_LINEAR)
            #inputimg = cv2.resize(inputimg, (1920,1080))
            now = datetime.now()
            dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
            image_url = "/home/r.ravishankar/Desktop/references/dataset/"+dt_string+"_"+str(imagecnt)+".jpg"
            cv2.imwrite(image_url, inputimg)
            cv2.namedWindow('title', cv2.WINDOW_NORMAL)
            cv2.imshow('title', inputimg)
            k = cv2.waitKey(1)
            if k == 27:
                break
    camera.Disconnect()

        

    
    

