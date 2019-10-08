#import os
#import io
#import Image
#from array import array
#import cv2
#import numpy as np

def imageproc(arr):
    frame = Image.open(io.BytesIO(arr))

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    frame = cv2.resize(frame, (600, 400))

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8)
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
    # display the detected boxes in the colour picture
    cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                                    
    
