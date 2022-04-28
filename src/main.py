import cv2
from cvzone.HandTrackingModule import HandDetector
from pprint import pprint as pp
import socket

#parameters
weidth, height=1280,720

#webcam
cap=cv2.VideoCapture(0)
cap.set(3,weidth)
cap.set(4,height)

#detector hand
detector= HandDetector(maxHands=1,detectionCon=0.8)

#communication
sock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverAddressPort=("127.0.0.1", 5052)

while True:
    #Get the Frame from webcam
    sucess,img= cap.read()
    data = []
    #Hands
    hands,img=detector.findHands(img)

    #landmark values (x,y,x)*21
    if hands:
        #get the 1st hand detected
        hand=hands[0]
        #get the landmark  list

        if 'lmList' in hand:
            lmlist = hand['lmList']
            #print(lmlist)
            for lm in lmlist:
                data.extend([lm[0],height-lm[1],lm[2]])
            print(data)
            sock.sendto(str.encode(str(data)),serverAddressPort)

    img = cv2.resize(img, (0,0) , None, 0.5, 0.5)
    cv2.imshow("Image",img)
    cv2.waitKey(1)