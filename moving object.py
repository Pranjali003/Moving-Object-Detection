import cv2
import time
import imutils

# Initialize the webcam
cam = cv2.VideoCapture(0)
time.sleep(1)

if not cam.isOpened():
    print("Error: Could not open camera.")
    exit()

firstFrame = None
area = 500  # Minimum area for motion detection

while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    text = "No Object Detected"  # Default message when no object is detected
    img = imutils.resize(img, width=500)
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussianImg = cv2.GaussianBlur(grayImg, (21, 21), 0)
    
    if firstFrame is None:
        firstFrame = gaussianImg
        continue
    
    imgDiff = cv2.absdiff(firstFrame, gaussianImg)
    threshImg = cv2.threshold(imgDiff, 25, 255, cv2.THRESH_BINARY)[1]
    threshImg = cv2.dilate(threshImg, None, iterations=2)
    cnts = cv2.findContours(threshImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # Loop over the contours and detect motion
    motion_detected = False
    for c in cnts:
        if cv2.contourArea(c) < area:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Moving Object Detected"  # Update message when an object is detected
        motion_detected = True
    
    # If no motion is detected, show "No Object Detected"
    if not motion_detected:
        text = "No Object Detected"
    
    # Display the status text on the frame
    cv2.putText(img, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("cameraFeed", img)
    
    # Exit if 'q' key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release the camera and close all windows
cam.release()
cv2.destroyAllWindows()

