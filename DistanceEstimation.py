import cv2 as cv 
import numpy as np

# Distance constants 
KNOWN_DISTANCE = 45 #INCHES
PERSON_WIDTH = 16 #INCHES
MOBILE_WIDTH = 3.14 #INCHES
STOP_SIGN_WIDTH = 30
CAR_WIDTH= 5.8

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
classesToDetectIndexes = [0, 2, 11, 67]

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

# object detector funciton /method
def object_detector(image):
    
    classes, scores, boxes = model.detect(image, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    # creating empty list to add objects data
    data_list = {}

    for (classid, score, box) in zip(classes, scores, boxes):
        # define color of each, object based on its class id 
        color= COLORS[int(classid) % len(COLORS)]
    
        label = "%s : %f" % (class_names[classid], score)

        # draw rectangle on and label on object
        cv.rectangle(image, box, color, 2)
        cv.putText(image, label, (box[0], box[1]-14), FONTS, 0.5, color, 2)

        className = class_names[classid]
        print(className)
        if className not in recObjects:
            recObjects.append(className)

        # getting the data 
        # 1: class name  2: object width in pixels, 3: position where have to draw text(distance)
        if classid in classesToDetectIndexes: # person class id 
            data_list[className] = {
                'width': box[2],
                'textPos': (box[0], box[1]-2)
            }
        # if you want inclulde more classes then you have to simply add more [elif] statements here
        # returning list containing the object data. 
    return data_list

def focal_length_finder (measured_distance, real_width, width_in_rf):
    focal_length = (width_in_rf * measured_distance) / real_width

    return focal_length

# distance finder function 
def distance_finder(focal_length, real_object_width, width_in_frmae):
    distance = (real_object_width * focal_length) / width_in_frmae
    return distance

# reading the reference image from dir 
ref_person = cv.imread('ReferenceImages/image14.png')
ref_mobile = cv.imread('ReferenceImages/image4.png')
ref_stop_sign = cv.imread('ReferenceImages/STOP_sign.png')
ref_car = cv.imread('ReferenceImages/audi.png')

mobile_data = object_detector(ref_mobile)
mobile_width_in_rf = mobile_data['cell phone']['width']

person_data = object_detector(ref_person)
person_width_in_rf = person_data['person']['width']

stop_sign_data = object_detector(ref_stop_sign)
stop_sign_width_in_rf = stop_sign_data['stop sign']['width']

car_data = object_detector(ref_car)
car_width_in_rf = car_data['car']['width']
print(f"Person width in pixels : {person_width_in_rf}\nmobile width in pixel: {mobile_width_in_rf}\nstop sign width in pixel: {stop_sign_width_in_rf}")

# finding focal length 
focal_person = focal_length_finder(KNOWN_DISTANCE, PERSON_WIDTH, person_width_in_rf)

focal_mobile = focal_length_finder(KNOWN_DISTANCE, MOBILE_WIDTH, mobile_width_in_rf)

focal_stop_sign = focal_length_finder(KNOWN_DISTANCE, STOP_SIGN_WIDTH, stop_sign_width_in_rf)

focal_car = focal_length_finder(KNOWN_DISTANCE, CAR_WIDTH, car_width_in_rf)

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    # cv.rectangle(frame, (20, 10-3), (20+150, 10+23), ,-1 )
    cv.putText(frame, f'Dis: {round(100,2)} inch', (20+5, 10+13), FONTS, 0.3, GREEN, 1)

    data = object_detector(frame)
    if 'person' in data:
        distance = distance_finder(focal_person, PERSON_WIDTH, data['person']['width'])
        x, y = data['person']['textPos']
        
        # cv.rectangle(frame, (x, y-3), (x+150, y+23),BLACK,-1 )
        cv.putText(frame, f'Dis: {round(distance,2)} inch', (x+5,y+13), FONTS, 0.48, GREEN, FONT_THICKNESS)
    elif 'cell phone' in data:
        distance = distance_finder (focal_mobile, MOBILE_WIDTH, data['cell phone']['width'])
        x, y = data['cell phone']['textPos']
    
        # cv.rectangle(frame, (x, y-3), (x+150, y+23),BLACK,-1 )
        cv.putText(frame, f'Dis: {round(distance,2)} inch', (x+5,y+13), FONTS, 0.48, GREEN, FONT_THICKNESS)
    elif 'stop sign' in data:
        distance = distance_finder (focal_stop_sign, STOP_SIGN_WIDTH, data['stop sign']['width'])
        
        if distance < 25:
            DISTANCE_TEXT_COLOR = AWARENESS_COLORS[0]
        if distance < 50 and distance > 25:
            DISTANCE_TEXT_COLOR = AWARENESS_COLORS[1]
        if distance > 50:
            DISTANCE_TEXT_COLOR = AWARENESS_COLORS[2]

        x, y = data['stop sign']['textPos']
    
        # cv.rectangle(frame, (x, y-3), (x+150, y+23),BLACK,-1 )
        cv.putText(frame, f'Расст: {round(formatInchToMeter(distance), 3)} м', (x+5,y+13), FONTS, 0.48, DISTANCE_TEXT_COLOR, FONT_THICKNESS)
    elif 'car' in data:
        distance = distance_finder (focal_car, CAR_WIDTH, data['car']['width'])
        
        if distance < 25:
            DISTANCE_TEXT_COLOR = AWARENESS_COLORS[0]
        if distance < 50 and distance > 25:
            DISTANCE_TEXT_COLOR = AWARENESS_COLORS[1]
        if distance > 50:
            DISTANCE_TEXT_COLOR = AWARENESS_COLORS[2]

        x, y = data['car']['textPos']
    
        # cv.rectangle(frame, (x, y-3), (x+150, y+23),BLACK,-1 )
        cv.putText(frame, f'Расст: {round(formatInchToMeter(distance), 3)} м', (x+5,y+13), FONTS, 0.48, DISTANCE_TEXT_COLOR, FONT_THICKNESS)

    cv.imshow('frame',frame)
    
    key = cv.waitKey(1)
    if key ==ord('q'):
        print(recObjects)
        break
cv.destroyAllWindows()
cap.release()

