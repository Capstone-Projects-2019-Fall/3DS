#Module Purpose: Detect if a driver’s eyes become tired, close, or turn away from the road
import cv2
from imageai.Detection import ObjectDetection
import os
from multiprocessing import Process

cap = cv2.VideoCapture(0)


def findPhones():
    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel(detection_speed="faster")
    #custom_objects = detector.CustomObjects(person=True, cell_phone=True)
    while(1):
        try:
            detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "test45.jpg"), output_image_path=os.path.join(execution_path , "imagenew.jpg"))
            for eachObject in detections:
                print(eachObject['name'])
        except ValueError:
            print('bad file')



# Pre-Conditions: A person must be within the frame of the camera
# Post-Conditions: None
# Parameters: face_cascade, eye_cascade, min_size
    # Face_cascade: Open_CV built-in haar cascade classifier for detecting human faces in a frame
    # eye_cascade: Open_CV built-in haar cascade classifier for detecting human eyes in a frame
    # Min_size: The minimum radius required in eye detection for the eyes to be considered detected. E.g. if eyes are closed, the radius will be smaller than min-size, so eyes will not be detected
# Return value: Boolean, is True if eyes are detected within the frame, is false otherwise
def findEyes():
    face_cascPath = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'
    eye_cascPath= cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml'  #face detect model
    faceCascade = cv2.CascadeClassifier(face_cascPath)
    eyeCascade = cv2.CascadeClassifier(eye_cascPath)
    min_size = 25

    while 1:
        ret, img = cap.read()

        frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(min_size, min_size),
            # flags = cv2.CV_HAAR_SCALE_IMAGE
        )
        # print("Found {0} faces!".format(len(faces)))
        if len(faces) == 0:
            pass
        elif len(faces) > 0:
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            #frame_tmp = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1, :]
            #frame = frame[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]
                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 3)
            roi=img[y:y+h, x:x+w]
            roi_gray=frame[y:y+h, x:x+w]
            eyes = eyeCascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(min_size, min_size),
                # flags = cv2.CV_HAAR_SCALE_IMAGE
            )
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)
            if len(eyes) == 0:
                pass

            else:
                pass

            #frame_tmp = cv2.resize(frame_tmp, (400, 400), interpolation=cv2.INTER_LINEAR)
        cv2.imshow('Face Recognition', img)

        waitkey = cv2.waitKey(1)

        if waitkey == ord('q') or waitkey == ord('Q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    t1 = Process(target=findPhones)
    t2 = Process(target=findEyes)
    t1.start()
    t2.start()
