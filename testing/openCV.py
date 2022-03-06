#import cv2 as cv
# initialize the camera
#cam = cv.VideoCapture(0)   # 0 -> index of camera
#s, img = cam.read()
#if s:    # frame captured without any errors
#    cv.namedWindow("cam-test")
#    cv.imshow("cam-test",img)
#    cv.waitKey(0)
#    cv.destroyWindow("cam-test")
#    cv.imwrite("filename.jpg", img) #save image

import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)

print(cap.get(3))
print(cap.get(4))
print(cap.get(15))

cap.set(3,1280)
cap.set(4,1024)
cap.set(15, -7)

print(cap.get(3))
print(cap.get(4))
print(cap.get(15))

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.rectangle(gray, (100, 100), (200, 200), (36, 255, 12), 2)
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
    if cv.waitKey(1) == ord('c'):
        cv.imwrite("capture.jpg", gray)
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()