import cv2
import numpy as np
import math
import socket
import threading

HOST = '192.168.125.4'
PORT = 8004
Real_X = 0
Real_Y = 0
X_stam = 0
Y_stam = 0
X_broc = 0
Y_broc = 0
Sem = True
ReadyToWrite = 0
RobotConnected = False
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_EXPOSURE,40)
FrameCounter = 0
_, Frame = cap.read()
#cap.set(cv2.CAP_PROP_EXPOSURE,1)
if (RobotConnected):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    sock.bind((HOST, PORT))
    print('Socket bind complete')
    sock.listen(10)
    print('Socket now listening')
    conn, addr = sock.accept()

def main() :
    global Real_X, Real_Y, X_stam, Y_stam, X_broc, Y_broc, RobotConnected, ReadyToWrite,cap
    ThreadStam = threading.Thread(target=StamVision)
    ThreadBroc = threading.Thread(target=BrocVision)
    ThreadBroc.start()
    ThreadStam.start()
    if(RobotConnected):
        ThreadRobotRead = threading.Thread(target=WaitForReady)
        ThreadRobotRead.start()

    DeltaY = 0
    DeltaX = 0
    while True:
        if (X_stam > X_broc):
            DeltaX = X_stam - X_broc
        else:
            DeltaX = X_broc - X_stam
        if (Y_stam > Y_broc):
            DeltaY = Y_stam - Y_broc
        else:
            DeltaX = Y_broc - Y_stam

        if (DeltaX != 0 and DeltaY != 0):
            Alpha = (math.atan(DeltaY / DeltaX) * (180/3.1415))

            #print("DeltaX=" + str(DeltaX))
            #print("DeltaY=" + str(DeltaY))
            print("Y=" + str(Y_broc))
            #print("X=" + str(X_broc))
            #print(Y_broc)

        if(RobotConnected):
            rInfo = str(Real_X) + str('@') + str(Real_Y)
            if (ReadyToWrite == 1):
                if Real_X < 565 and Real_X > 100:
                    print('sending')
                    message = bytes(str(rInfo), 'utf8')
                    conn.send(message)
                    message = ''
                    ReadyToWrite = 0
                else:
                    print('Broccoli out of range')

        k = cv2.waitKey(30)
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()


def GetCameraImage():
    global Sem, cap, FrameCounter, Frame

    while Sem == False:
        pass
    Sem = False
    if(FrameCounter % 2 == 0):
        _, Frame = cap.read()
    FrameCounter = FrameCounter + 1
    Sem = True

    return Frame


def BrocVision():
    global Real_X , X_broc, Y_broc, Real_Y

    while True:
        frame = GetCameraImage()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV, 0)
        hsv = cv2.medianBlur(hsv, 11)

        lower_red_broc = np.array([0, 197, 0])
        upper_red_broc = np.array([38, 255, 208])
        mask_broc = cv2.inRange(hsv, lower_red_broc, upper_red_broc)
        res_broc = cv2.bitwise_and(frame, frame, mask=mask_broc)

        kernel = np.ones((5, 5), np.uint8)
        mask_broc = cv2.dilate(mask_broc, kernel, iterations=1)
        mask_broc = cv2.erode(mask_broc, kernel, iterations=7)
        mask_broc = cv2.dilate(mask_broc, kernel, iterations=2)
        mask_broc = cv2.erode(mask_broc, kernel, iterations=5)
        mask_broc = cv2.dilate(mask_broc, kernel, iterations=9)

        _, contours_broc, hierarchy_broc = cv2.findContours(mask_broc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours_broc:
            cnt = contours_broc[0]
            area = cv2.contourArea(cnt)
            if area > 5000:
                cv2.drawContours(frame, contours_broc, 0, (255, 0, 255), 3)
                M = cv2.moments(cnt)
                if area > 5000:
                    X_broc = int(M['m10'] / M['m00'])
                    Y_broc = int(M['m01'] / M['m00'])
                    cv2.circle(frame, (X_broc, Y_broc), 10, (0, 0, 255), -1)
                    Real_X = int(X_broc * -2.64 + 1212.84)
                    Real_Y = int(Y_broc * 3.12 - 197.32)

        cv2.imshow('fgbg_broc', mask_broc)
        cv2.imshow('res_broc', res_broc)
        cv2.imshow('Original_ broc', frame)
        k = cv2.waitKey(30)

def StamVision():
    global X_stam, Y_stam

    while True:
        frame = GetCameraImage()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV, 0)
        hsv = cv2.medianBlur(hsv, 11)

        lower_red_stam = np.array([0, 0, 231])
        upper_red_stam = np.array([31, 255, 255])
        mask_stam = cv2.inRange(hsv, lower_red_stam, upper_red_stam)
        res_stam = cv2.bitwise_and(frame, frame, mask=mask_stam)

        kernel = np.ones((5, 5), np.uint8)
        mask_stam = cv2.dilate(mask_stam, kernel, iterations=1)
        mask_stam = cv2.erode(mask_stam, kernel, iterations=10)
        mask_stam = cv2.dilate(mask_stam, kernel, iterations=17)

        _, contours_stam, hierarchy_stam = cv2.findContours(mask_stam, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours_stam:
            cnt = contours_stam[0]
            area = cv2.contourArea(cnt)
            if area > 3000:
                cv2.drawContours(frame, contours_stam, -1, (0, 255, 255), 3)
                M = cv2.moments(cnt)
                if area > 3000:
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    X_stam = int(M['m10'] / M['m00'])
                    Y_stam = int(M['m01'] / M['m00'])
                    cv2.circle(frame, (X_stam, Y_stam), 10, (0, 0, 255), -1)

        cv2.imshow('fgbg_stam', mask_stam)
        cv2.imshow('res', res_stam)
        cv2.imshow('Original_ stam', frame)
        k = cv2.waitKey(30)

def WaitForReady():
    global ReadyToWrite
    global conn
    print('entered function')
    while True:
        # print('reading check :',ReadyToWrite)
        if (ReadyToWrite == 0):
            received = conn.recv(256)
            print (received.decode())
            if received.decode() == 'ready':
                ReadyToWrite = 1
                print ('ready received')
                received = ''


if __name__=="__main__":
    main()