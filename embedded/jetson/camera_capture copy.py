import os
import cv2
import time

# Camera Capture
# Parameter: sleep time, num of captures
def CamCapture_window(directory, sleepTime=1, numCaptures=5,imageFile='id'):
    #Check able to use camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("WebCam is closed")
        return
    
    #Make Directory diractory name is id for one person
    #if id directory exists
    if os.path.exists(directory):
        print("ID exists, Please use new ID")
        return
    os.makedirs(directory)

    startTime = time.time()
    frameCounter = 0

    while frameCounter < numCaptures:
        ret, frame = cap.read()
        if not ret:
            print("Can't read frame")
            break
        currentTime = time.time()
        if currentTime - startTime >= sleepTime:
            imageFileNameIndex = f'{directory}/{imageFile}_{frameCounter}.jpg'
            cv2.imwrite(imageFileNameIndex, frame)
            frameCounter += 1
            startTime = currentTime

    cap.release()

def main():
    CamCapture_window(directory='id')

if __name__ == "__main__":
    main()

