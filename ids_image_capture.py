#Image capturing from ids camera 

import ids_peak.ids_peak as ids_peak
import ids_peak_ipl.ids_peak_ipl as ids_ipl
import ids_peak.ids_peak_ipl_extension as ids_ipl_extension
from matplotlib import pyplot as plt
import numpy as np
import cv2

def set_exposure(remote_device_nodemap, exposure_time_us):
    """
    Set the exposure time of the camera.
    """
    try:
        exposure_node = remote_device_nodemap.FindNode("ExposureTime")
        if exposure_node is not None:
            exposure_node.Value = exposure_time_us
            print(f"Exposure time set to {exposure_time_us} us")
        else:
            print("ExposureTime node not found.")
    except Exception as e:
        print(f"Error setting exposure time: {e}")

def main():
    # Initialize IDS peak library
    ids_peak.Library.Initialize()

    try:
        # Device manager setup
        device_manager = ids_peak.DeviceManager.Instance()
        device_manager.Update()
        device_descriptors = device_manager.Devices()
        print("Found Devices: " + str(len(device_descriptors)))
        
        for device_descriptor in device_descriptors:
            print(device_descriptor.DisplayName())
        
        if not device_descriptors:
            raise RuntimeError("No devices found.")
        
        # Open the first device
        device = device_descriptors[0].OpenDevice(ids_peak.DeviceAccessType_Control)
        print("Opened Device: " + device.DisplayName())
        
        # Configure data stream
        datastream = device.DataStreams()[0].OpenDataStream()
        remote_device_nodemap = device.RemoteDevice().NodeMaps()[0]

        payload_size = remote_device_nodemap.FindNode("PayloadSize").Value()
        for _ in range(datastream.NumBuffersAnnouncedMinRequired()):
            buffer = datastream.AllocAndAnnounceBuffer(payload_size)
            datastream.QueueBuffer(buffer)

        datastream.StartAcquisition()
        remote_device_nodemap.FindNode("AcquisitionStart").Execute()
        remote_device_nodemap.FindNode("AcquisitionMode").SetCurrentEntry("Continuous")
        #remote_device_nodemap.FinNode("AutoFocus").SetCurrentEntry("Off")
        # remote_device_nodemap.FindNode("TriggerSelector").SetCurrentEntry("ExposureStart")
        remote_device_nodemap.FindNode("TriggerSource").SetCurrentEntry("Software")
        #remote_device_nodemap.FindNode("TriggerMode").SetCurrentEntry("On")
        # Set exposure time (in microseconds)
        exposure_time_us = 10  # Example: 10 milliseconds
        set_exposure(remote_device_nodemap, exposure_time_us)

        while True:
            print("Capturing data...")
            # Trigger image capture
            remote_device_nodemap.FindNode("TriggerSoftware").Execute()
            buffer = datastream.WaitForFinishedBuffer(5000)
            
            if buffer is None:
                print("No buffer received.")
                continue

            raw_image = ids_ipl_extension.BufferToImage(buffer)
            color_image = raw_image.ConvertTo(ids_ipl.PixelFormatName_RGB8, ids_ipl.ConversionMode_Fast)

            datastream.QueueBuffer(buffer)

            # Convert image to numpy array and display it
            picture = color_image.get_numpy_3D()
            #picture = cv2.resize(picture, (640,480))
            cv2.imshow("Image", picture)

            # Wait for a key press; press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Stop acquisition and clean up
        remote_device_nodemap.FindNode("AcquisitionStop").Execute()
        datastream.StopAcquisition()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure proper library closure
        ids_peak.Library.Close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
