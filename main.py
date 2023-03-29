import cv2 as cv 
import numpy as np

# Distance constants (INCHES) 
KNOWN_DISTANCE = 8
CUP_WIDTH = 3.5

# Object detector constant 
CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.3

# colors for object detected
COLORS = [(255,0,0),(255,0,255),(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
GREEN =(0,255,0)
BLACK =(0,0,0)

# defining fonts
FONTS = cv.FONT_HERSHEY_COMPLEX
FONT_THICKNESS = 1
AWARENESS_COLORS = [(0, 0, 255), (0, 215, 255), (0,255,0)]

# getting class names from classes.txt file 
class_names = []
recObjects = []
classesToDetectIndexes = [41]

with open("classes.txt", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

#  setttng up opencv net
yoloNet = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')

yoloNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
yoloNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

model = cv.dnn_DetectionModel(yoloNet)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

def formatInchToMeter(value):
    return value / 39.37

def formatMeterToInch(value):
    return value * 39.37

def getColor(distance):
    if distance < 25:
        DISTANCE_TEXT_COLOR = AWARENESS_COLORS[0]
    if distance < 50 and distance > 25:
        DISTANCE_TEXT_COLOR = AWARENESS_COLORS[1]
    if distance > 50:
        DISTANCE_TEXT_COLOR = AWARENESS_COLORS[2]
    return DISTANCE_TEXT_COLOR

# object detector funciton /method
def object_detector(image):
    classes, scores, boxes = model.detect(image, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    # creating empty list to add objects data
    data_list = {}

    for (classid, score, box) in zip(classes, scores, boxes):
        # define color of each, object based on its class id 
        color= COLORS[int(classid) % len(COLORS)]
        label = "%s : %f" % (class_names[classid[0]], score)

        # draw rectangle on and label on object
        cv.rectangle(image, box, color, 2)
        cv.putText(image, label, (box[0], box[1]-14), FONTS, 0.5, color, 2)

        className = class_names[classid[0]]
        if className not in recObjects:
            recObjects.append(className)

        # if classid in classesToDetectIndexes: 
        data_list[className] = {
            'width': box[2],
            'textPos': (box[0], box[1]-2)
        } 
    return data_list

def focal_length_finder (measured_distance, real_width, width_in_rf):
    focal_length = (width_in_rf * measured_distance) / real_width
    return focal_length

def distance_finder(focal_length, real_object_width, width_in_frmae):
    distance = (real_object_width * focal_length) / width_in_frmae
    return distance



def run_video(name: str, width: float, distance: float, img_path: str, video_path: str):
    ref_image = cv.imread(img_path)
    image_data = object_detector(ref_image)

    object_width_in_rf = image_data[name]['width']

    focal_length = focal_length_finder(distance, width, object_width_in_rf)

    cap = cv.VideoCapture(video_path)
    

    # cap = cv.resize(cap_raw, (300, 300))
    while True:
        ret, frame = cap.read()
        # frame = cv.resize(f, (270, 480))

        # cv.putText(
        #     frame,
        #     f'Dis: {round(100,2)} inch',
        #     (20+5, 10+13),
        #     FONTS,
        #     0.3,
        #     GREEN,
        #     1
        # )

        data = object_detector(frame)

        if name in data:
            measured_distance = distance_finder(focal_length, width, data[name]['width'])
            DISTANCE_TEXT_COLOR = getColor(measured_distance)
            x, y = data[name]['textPos']

            cv.putText(
                frame, 
                f'Расст: {round(formatInchToMeter(measured_distance), 3)} м', 
                (x+5,y+13), 
                FONTS, 
                0.48, 
                DISTANCE_TEXT_COLOR, 
                FONT_THICKNESS
            )
    
        cv.imshow('frame',frame)
        
        key = cv.waitKey(1)

        if key == ord('q'):
            print(recObjects)
            break
        if key == ord('p'):
            cv.waitKey(-1)

    cv.destroyAllWindows()
    cap.release()