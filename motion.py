from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
import sendEmail
disarmed = False
def stop():
    disarmed = True
def start(addr, passwd, server):
    ##Setup Camera 
    camera = PiCamera()
    camera.resolution = (736,480)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size = (736,480))

    ##Need to warmup camera first
    sleep(0.2)

    ##Need to take first picture of the scenario (used to compare consecutived frames for motion detection)
    ##The picture is transformed into a black and white blurred version for easier comparison
    camera.capture(rawCapture, format ="bgr")
    prevImage = rawCapture.array
    prevGray = cv2.cvtColor(prevImage, cv2.COLOR_BGR2GRAY)
    prevGray = cv2.GaussianBlur(prevGray, (21,21), 0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    ##Used to construct the motion videos.
    out = cv2.VideoWriter('feed.avi', fourcc, 5.0, (736, 480))
    rawCapture.truncate(0) ##Free the camera buffer
    counter = 0 ##Used to count number of frames where movement was detected
    recording = False

    ## Run forever
    for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):
        motion = False
        image = frame.array ##Get current image

        ##Transform it into a gray blurred version
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21,21), 0)

        ##Compare current image with previous one
        frameDelta = cv2.absdiff(prevGray, gray)
        threshold = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    
        threshold = cv2.dilate(threshold, None, iterations = 2)
        (_, cnts, _) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow('feed',image)
        ##For every difference in the images
        for c in cnts:
            if cv2.contourArea(c) < 500:
                continue
                motion = True
                counter = counter + 1
        
        
        key = cv2.waitKey(1) & 0xFF
        prevGray = gray
        rawCapture.truncate(0)
        ##If there has been motion for more than three frames write to the video
        if motion and counter > 3:
            recording = True
            flipped = cv2.flip(image,-1)
            out.write(flipped)

        ##If there is no motion reset counter to 0
        if not motion:
            ##If there is no motion but the camera was recording send an email
            if recording:
                out.release()
                sendEmail.sendEmail(addr, passwd, server)
                recording = False
                out.open('feed.avi',fourcc,5.0,(736,480))
            counter = 0
        if disarmed:
            break
