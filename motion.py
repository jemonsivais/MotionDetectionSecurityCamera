from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import datetime
import imutils
import sendEmail

camera = PiCamera()
camera.resolution = (736,480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size = (736,480))
    
time.sleep(0.2)
camera.capture(rawCapture, format ="bgr")
prevImage = rawCapture.array
prevGray = cv2.cvtColor(prevImage, cv2.COLOR_BGR2GRAY)
prevGray = cv2.GaussianBlur(prevGray, (21,21), 0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('feed.avi', fourcc, 10.0, (736, 480))
rawCapture.truncate(0)
counter = 0
recording = False

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):
    motion = False
    image = frame.array
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)
        
    frameDelta = cv2.absdiff(prevGray, gray)
    threshold = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    
    threshold = cv2.dilate(threshold, None, iterations = 2)
    (_, cnts, _) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in cnts:
        if cv2.contourArea(c) < 500:
            continue
        motion = True
        counter = counter + 1
        
        
    cv2.imshow("Security Feed", image)
    key = cv2.waitKey(1) & 0xFF
    prevGray = gray
    rawCapture.truncate(0)
    if motion and counter > 3:
        recording = True
        flipped = cv2.flip(image,-1)
        out.write(flipped)
        
    if not motion:
        if recording:
            out.release()
            sendEmail.sendEmail()
            recording = False
            out.open('feed.avi',fourcc,10.0,(736,480))
        counter = 0
    if key == ord("q"):
        break
