# This code is written at chaowei. It is based on the OpenCV project. It is subject to the license terms in the LICENSE file found in this distribution and at http://opencv.org/license.html

# Usage example:  python3 object_detection_yolo.py --video=run.mp4
#                 python3 object_detection_yolo.py --image=bird.jpg

import cv2 as cv
# import argparse
import sys
import numpy as np
import os.path
import argparse
# from scipy.spatial import Delaunay
# import matplotlib.pyplot as plt

# Initialize the parameters
confThreshold = 0.3  # Confidence threshold
nmsThreshold = 0.3  # Non-maximum suppression threshold
inpWidth = 416  # Width of network's input image
inpHeight = 416  # Height of network's input image
current_path = os.getcwd()

# Load names of classes
# classesFile = "/Users/jiguang/my_disk/keras-yolo3-master/my_folder/voc-bm.names";
classesFile = "/home/dcm360/object-detection/weights/voc.names";

classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "/home/dcm360/object-detection/weights/yolov3-voc.cfg";

modelWeights = "/home/dcm360/object-detection/weights/yolov3-voc_51000.weights";

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Draw the predicted bounding box
def drawPred(frame, classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    # cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 1)
   # labelName = classes[classId]
   # if labelName == 'green':
   #     cv.rectangle(frame, (left, top), (right, bottom), (31,255,60), 1)
   # elif labelName == 'red':
   #     cv.rectangle(frame, (left, top), (right, bottom), (255,0,255), 1)
   
    labelName = classes[classId]
    if labelName == 'yellow':
        cv.rectangle(frame, (left, top), (right, bottom), (31, 255, 60), 1)
    elif labelName == 'orange':
        cv.rectangle(frame, (left, top), (right, bottom), (255, 0, 255), 1)
    elif labelName == 'blue':
        cv.rectangle(frame, (left, top), (right, bottom), (255, 0, 255), 1)
   # box边框
   # else:
    #    cv.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 1)

    # cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        # label = '%s:%s' % (classes[classId], label)
        # label = '%s:%s' % (classes[classId], label)
        label = classes[classId]

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])

    #字体上的幕布
    # cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
    #              (255, 255, 255), cv.FILLED)
    cv.putText(frame, label[0], (left, int(top-0.01*top)), cv.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255),1)


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs, img_path):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            # print(len(detection))
            # print(classId)
            # if (classId>0):
            #     print(classId)
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
##      存储info为txt文件
    box_infor = []
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(frame,classIds[i], confidences[i], left, top, left + width, top + height)
        assert (classIds[i] < len(classes))
        # label = '%s:%s' % (classes[classId], label)
        # label = '%s:%s' % (classes[classId], label)
        label_names = classes[classIds[i]]


        #if label_names != 'box':
            #box_infor.insert(0,[str(label_names), str(left), str(top), str(left + width),str(top + height)])
       # else:
            # box_infor.append([str(label_names), str(left), str(top), str(left + width), str(top + height), '\n'])
        box_infor.append([str(label_names), str(left), str(top), str(left + width), str(top + height)])
        # print([str(label_names), str(left), str(top), str(left + width), str(top + height)])
#打印坐标,除了box以外的所有做坐标
    new_label_names = []
    points = []
    for i in box_infor:
        #返回点的坐标
        points.append(i[3:])
        # 返回点的颜色
        new_label_names.append(i[0])
    return points,new_label_names

def output_points01(img_path):
    # outputFile = "yolo_out_py.avi"
    if (img_path):
        # Open the image file
        if not os.path.isfile(img_path):
            print("Input image file ", img_path, " doesn't exist")
            sys.exit(1)
        cap = cv.VideoCapture(img_path)
       # outputFile = img_path[:-4] + '.png'
        outputFile = img_path.split('.')[-2]+ '.png'
        # outputFile = img_path[:-4] + '.jpg'

    # Get the video writer initialized to save the output video
    if (not img_path):
        vid_writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30,
                                    (round(cap.get(cv.CAP_PROP_FRAME_WIDTH)), round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

    while cv.waitKey(1) < 0:

        # get frame from the video
        hasFrame, frame = cap.read()

        # Stop the program if reached end of video
        if not hasFrame:
            # print("Done processing !!!")
            # print("Output file is stored as ", outputFile)
            # cv.waitKey(30000)
            # Release device
            cap.release()
            break

        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = net.forward(getOutputsNames(net))

        #返回点的坐标和颜色
        infor = postprocess(frame, outs, img_path)
        label_names = infor[1]
        points = infor[0]

        # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.2, (0, 0, 255))

        # Write the frame with the detection boxes


        #为data2json返回识别后的图片路径+名称
        #存贮图片
        if (img_path):
            path = outputFile.split('/')[-1]
            new_path = '/var/www/static/recognize/original/recognize_img/'+path
            #new_path = '/var/www/html/static/recognize/original/recognize_img/'+path
            # new_path = '/Users/jiguang/img_path/'+path
            print(new_path)
            cv.imwrite(new_path, frame.astype(np.uint8));
        return points, label_names



def output_points(image_path):
    def get_img_file(file_name):
        imagelist = []
        for parent, dirnames, filenames in os.walk(file_name):
            for filename in filenames:
                if filename.lower().endswith(
                        ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                    imagelist.append(os.path.join(parent, filename))
            return imagelist

    points_label_names = []
    img_list = get_img_file(image_path)
    for i in img_list:
        # label_name = []
        # point = []
        # r = detect(net, meta, i.encode('utf-8'))
        #pic_id = i.split("/")[-1][0:5]
        pic_id = i.split("/")[-1][3:8]
        res = output_points01(i)
        point = res[0]
        label_name = res[1]
        # label_name = list(res[1])
        points_label_names.append([pic_id,point,label_name])
    # print(points_label_names)
    return points_label_names
