import torch
import os
import cv2
from ultralytics.utils.plotting import Annotator, colors, save_one_box
import numpy as np
import json
import time

yolov5_model = 'D:/Dev/yolov5_v1.0/yolov5_v1.0/runs/train/exp18/weights/last.pt'
device = 'cpu'  # Set to 'cpu' or '0' for GPU

# Load the YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)
model = torch.hub.load('ultralytics/yolov5', 'custom', yolov5_model).to(device)

# Specify the directory where images will be saved
save_directory = 'frames'

# Create the directory if it doesn't exist
os.makedirs(save_directory, exist_ok=True)

# Frame capture rate (in seconds)
frame_capture_rate = 0.2  # Capture 5 frames per second

# Create a function to process incoming video frames and save them
def process_frame(img, frame_counter):
    # Decode the received frame
    #frame = cv2.imread("pcb1.jpg", cv2.IMREAD_COLOR)#cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
    results = model(img)
    # Save the frame with detected bounding boxes
    frame_with_boxes = results.render()[0]
    filename = os.path.join(save_directory, f"frame_{frame_counter}.jpg")
    cv2.imwrite(filename, frame_with_boxes)

    # Display the received frame with bounding boxes
    #results.show()
    output_json_file_path = os.path.join(save_directory, f"frame_{frame_counter}.json")
    print(results.pandas().xyxy[0])


    results.pandas().xyxy[0].to_json(output_json_file_path,orient='records', indent=2)
    print(results.pandas().xyxy[0])
    return output_json_file_path

def compare_json_objects(output_obj, master_obj):
    if output_obj["xmin"] == master_obj["xmin"] and \
       output_obj["ymin"] == master_obj["ymin"] and \
       output_obj["xmax"] == master_obj["xmax"] and \
       output_obj["ymax"] == master_obj["ymax"] and \
       output_obj["name"] == master_obj["name"]:
        return True
    else:
        return False

def compare_json_files(output_file_path, master_file_path):
    with open(output_file_path, 'r') as output_file:
        output_data = json.load(output_file)

    with open(master_file_path, 'r') as master_file:
        master_data = json.load(master_file)

    result_table = []
    for output_obj in output_data:
        component_name = output_obj["name"]
        status = False

        for master_obj in master_data:
            if compare_json_objects(output_obj, master_obj):
                status = True
                break

        result_table.append({"Component": component_name, "Status": status})

    return result_table
    
if __name__ == '__main__':
    
    folder = 'D:/test'#'D:/CV_Inspection/Hawk/HBLpcbs'
    master_json_file_path = "output.json"
    framecounter = 0
    for filename in os.listdir(folder):
        framecounter += 1
        i = 0
        img = cv2.imread(os.path.join(folder,filename))
        start = time.time()
        output_json_file_path = process_frame(img, framecounter)
        result_table = compare_json_files(output_json_file_path, master_json_file_path)
        end = time.time()
        processing_time = f"{(end-start)*10**3:.03f}ms"
        with open(output_json_file_path, 'r') as test_file:
            master_data = json.load(test_file)
        for result_row in result_table:
            master_data[i].update({'status':result_row['Status']})
            master_data[i].update({'processing_time':processing_time})
            i+=1
        with open(output_json_file_path, 'w', encoding='utf8') as outfile:
            json.dump(master_data, outfile, indent=2)