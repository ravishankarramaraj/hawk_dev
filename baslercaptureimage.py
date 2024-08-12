# conecting to the first available camera
from pypylon import pylon
from datetime import datetime
import time
import cv2

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
imagecnt = 0
while camera.IsGrabbing():
    imagecnt += 1
    grabResult = camera.RetrieveResult(50000, pylon.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        # Access the image data.
        # print("SizeX: ", grabResult.Width)
        # print("SizeY: ", grabResult.Height)
        image = converter.Convert(grabResult)
        img = image.Array
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S")
        image_url = "/home/r.ravishankar/Desktop/references/dataset/"+dt_string+"_"+str(imagecnt)+".jpg"
        img = cv2.resize(img, (1920,1080))
        cv2.imwrite(image_url, img)
        cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        cv2.imshow('title', img)
        k = cv2.waitKey(0)
        if k == 27:
            break
        #print("Gray value of first pixel: ", img[0, 0])

        grabResult.Release()
camera.Close()