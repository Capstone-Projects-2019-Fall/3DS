import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import pygame
import time

#Setup classifier

face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade=cv2.CascadeClassifier('haarcascade_eye.xml')
phone_cascade=cv2.CascadeClassifier("Phone_Cascade.xml")

speedFile = "speedData.txt"
fh = open(speedFile, "r")
print("Reading from speed file for presentation purposes.")
line = fh.readline()
line = line.strip('\n')
info = line.split(' ')
frequency = info[0]
seconds = info[1]

min_size = 18
start_time = 0
elapsed_time = 0

cap = PiCamera()
cap.resolution = (640, 480)
cap.framerate = 32
rawCap = PiRGBArray(cap, size=(640, 480))

pygame.mixer.init()
pygame.mixer.music.load("winxp.wav")
didDetect = False
moving = False


for frame in cap.capture_continuous(rawCap, format="bgr", use_video_port=True):
    hasPhone = False
    line = fh.readline()
    if(line == ''):
        print("End of speed file.")
        break
    line = line.strip('\n')
    info = line.split(' ')
    if(info[0] == "0.0"):
        if(moving):
            print("Not moving now.")
        moving = False
    else:
        if(not moving):
            print("Starting to move.")
        moving = True
    
    if(start_time != 0):
        elapsed_time = time.time() - start_time
    
    img = frame.array

    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Use classifier to detect faces
    faces=face_cascade.detectMultiScale(gray, 1.1, 1)

    phones=phone_cascade.detectMultiScale(gray, 3, 12)

    for (x,y,w,h) in phones:
        #cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,255), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'Phone',(x-w,y-h), font, 0.5, (11,255,255), 2, cv2.LINE_AA)
        hasPhone = True

    if len(faces) == 0:
        if(elapsed_time > 3 and start_time != 0 and moving):
            pygame.mixer.music.play()
            elapsed_time = 0
            start_time = 0
            pass
        else:
            pass
    elif len(faces) > 0:
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            pass
        #frame_tmp = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1, :]
        #frame = frame[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]
            #cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 3)
        roi=img[y:y+h, x:x+w]
        roi_gray=gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(min_size, min_size),
            # flags = cv2.CV_HAAR_SCALE_IMAGE
        )
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)
        if len(eyes) == 0:
            if(hasPhone and didDetect and moving):
                #pygame.mixer.music.play()
                print("Play")
                pass
            elif(elapsed_time > 3 and start_time != 0 and moving):
                pygame.mixer.music.play()
                elapsed_time = 0
                start_time = 0
                pass
            elif(didDetect):
                start_time = time.time()
                didDetect = False
                pass
            else:
                pass

        else:
            didDetect = True
            elapsed_time = 0
            start_time = 0
            pass

        #frame_tmp = cv2.resize(frame_tmp, (400, 400), interpolation=cv2.INTER_LINEAR)
    cv2.imshow('Face Recognition (Press Q to exit)', img)

    waitkey = cv2.waitKey(1)
    
    rawCap.truncate(0)

    if waitkey == ord('q') or waitkey == ord('Q'):
        break

cv2.destroyAllWindows()
fh.close()
