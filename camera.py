import cv2
import time

cam = cv2.VideoCapture(0)
time.sleep(1)
_,img= cam.read()
cv2.imwrite("imageframeCamera.jpg",img)
cam.release()
