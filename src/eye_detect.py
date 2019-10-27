
import cv2

face_cascPath = 'C:/Users/mattv/Anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml'
eye_cascPath= 'C:/Users/mattv/Anaconda3/Lib/site-packages/cv2/data/haarcascade_eye_tree_eyeglasses.xml'  #face detect model
faceCascade = cv2.CascadeClassifier(face_cascPath)
eyeCascade = cv2.CascadeClassifier(eye_cascPath)
min_size = 25

def findEyes(faceCascade, eyeCascade, min_size):
    cap = cv2.VideoCapture(0)
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
            print(0)
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
                print(0)

            else:
                print(1)

            #frame_tmp = cv2.resize(frame_tmp, (400, 400), interpolation=cv2.INTER_LINEAR)
        cv2.imshow('Face Recognition', img)

        waitkey = cv2.waitKey(1)

        if waitkey == ord('q') or waitkey == ord('Q'):
            cv2.destroyAllWindows()
            break

def main():
    findEyes(faceCascade, eyeCascade, min_size)

main()
