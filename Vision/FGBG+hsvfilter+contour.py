import cv2
import numpy as np
import socket
from threading import Thread

HOST = '192.168.125.4'		# Symbolic name, meaning all available interfaces
PORT = 8004  				# Arbitrary non-privileged port
ReadyToWrite = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# Bind socket to local host and port

sock.bind((HOST, PORT))
print('Socket now bind')

print('Socket bind complete')

# Start listening on socket
sock.listen(10)
print('Socket now listening')

conn, addr = sock.accept()

def WaitForReady():
    global ReadyToWrite
    global conn
    print('entered function')
    while True:
        #print('looping')
        print('reading check :',ReadyToWrite)
        if (ReadyToWrite == 0):
            #print('aan het lezen')
            received = conn.recv(256)
            print (received.decode())
            if received.decode() == 'ready':
                ReadyToWrite = 1
                print ('ready received')
                received = ''


cap = cv2.VideoCapture(1)
cv2.ocl.setUseOpenCL(False)
fgbg = cv2.createBackgroundSubtractorMOG2()

Threadje = Thread(target=WaitForReady)
Threadje.start()

while True:
    #print('in main while')
    _, frame = cap.read()
    frame = frame[150:380,0:450]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV, 0)

    lower_red = np.array([35, 17, 0])
    upper_red = np.array([87, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=3)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.erode(mask, kernel, iterations=4)
    mask = cv2.dilate(mask, kernel, iterations=5)


    fgmask = fgbg.apply(mask)

    _, contours, hierarchy = cv2.findContours(mask   , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        #print('contouyrs')
        cnt = contours[0]
        area = cv2.contourArea(cnt)
        if area > 0:
            cv2.drawContours(frame, contours, -1, (0, 255, 255), 3)
            M = cv2.moments(cnt)
            if area > 500:
                #print('grote area')
                #hull = cv2.convexHull(cnt)
                #epsilon = 0.1 * cv2.arcLength(cnt, True)
                #approx = cv2.approxPolyDP(cnt, epsilon, True)
                #cv2.drawContours(frame,[approx],0,(0,0,255),2)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
                #print("x=", cx, "y=", cy)
                array = [cx, cy]
                rx = int(cx*-2.1+1017.4)
                if rx>565:
                    rx = 565
                if rx<130:
                    rx = 130

                #print('voor check')
                if(ReadyToWrite == 1):
                    #print(str(rx))
                    message = bytes(str(rx),'utf8')
                    conn.send(message)
                    message = ''
                    ReadyToWrite = 0
                    print('sending check :',ReadyToWrite)

    cv2.imshow('Original', frame)
    cv2.imshow('fgbg', mask)
    cv2.imshow('res', res)



    k = cv2.waitKey(30)
    if k == 27:
        break


