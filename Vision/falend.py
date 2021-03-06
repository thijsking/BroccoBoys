import time
import cv2
import numpy as np
import math
import socket
import threading

HOST = '192.168.125.4'
PORT = 8004
CONVEYOR_SPEED = 500

Stam_Area = 0
Broc_Area = 0
Real_X = 0
Real_Y = 0
Real_StamX = 0
Real_StamY = 0
X_stam = 0
Y_stam = 0
X_broc = 0
Y_broc = 0
X_brocs = []
Y_brocs = []
Alpha_brocs = []
Time_brocs = []
Sem = True
ReadyToWrite = 0
RobotConnected = True
TimeBrocDetected = time.time()
cap = cv2.VideoCapture(0)
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

    while True :
        if(RobotConnected):
            if (ReadyToWrite == 1) and (len(X_brocs) > 0) and (len(Time_brocs) > 0):
                if(X_brocs[0] != 0):
                    if len(Time_brocs) > 1:
                        again = True
                        while(again and (len(Time_brocs) > 1)):
                            again = False
                            diff = Time_brocs[1] - Time_brocs[0]
                            print(diff)
                            if diff < 0.5:
                                #print("DELETING")
                                DeleteBroc(1)
                                again = True



                    TimeStamp = time.time()
                    DeltaTime = TimeStamp - Time_brocs[0]
                    X_Time = int(X_brocs[0] - DeltaTime * CONVEYOR_SPEED)
                    X_Move = int((1/3)*(4 * X_Time - 275) - (2/3)*math.sqrt(math.pow(X_Time,2) - 550 * X_Time + 75772))
                    rInfo = str(X_Move) + str('@') + str(Y_brocs[0]) + str('$') + str(Alpha_brocs[0])

                    if X_Move < -200:
                        print("to FAR")
                        DeleteBroc(0)

                    if X_Move > -150 and X_Move < 550:
                        print('sending ', rInfo)
                        message = bytes(str(rInfo), 'utf8')
                        conn.send(message)
                        message = ''
                        #DeleteBroc(0)
                        ReadyToWrite = 0
                        print(X_brocs)
                        Y_broc = 0

        k = cv2.waitKey(30)
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

def DeleteBroc(index):
    if(len(X_brocs)):
        del X_brocs[index]
        del Y_brocs[index]
        del Time_brocs[index]
        del Alpha_brocs[index]
        #print("deleting index ", index )

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
    global Real_X , X_broc, Y_broc, Real_Y, TimeBrocDetected, Broc_Area, Stam_Area, Real_StamY, Real_StamX, X_stam

    while True:
        frame = GetCameraImage()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV, 0)
        hsv = cv2.medianBlur(hsv, 11)

        lower_red_broc = np.array([0, 210, 0])
        upper_red_broc = np.array([38, 255, 192])
        mask_broc = cv2.inRange(hsv, lower_red_broc, upper_red_broc)
        res_broc = cv2.bitwise_and(frame, frame, mask=mask_broc)

        kernel = np.ones((5, 5), np.uint8)
        mask_broc = cv2.dilate(mask_broc, kernel, iterations=3)
        mask_broc = cv2.erode(mask_broc, kernel, iterations=7)
        mask_broc = cv2.dilate(mask_broc, kernel, iterations=2)
        mask_broc = cv2.erode(mask_broc, kernel, iterations=5)
        mask_broc = cv2.dilate(mask_broc, kernel, iterations=9)

        _, contours_broc, hierarchy_broc = cv2.findContours(mask_broc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours_broc:
            cnt = contours_broc[0]
            Broc_Area = cv2.contourArea(cnt)
            print("broc area ", Broc_Area)
            if Broc_Area > 5000:
                cv2.drawContours(frame, contours_broc, 0, (255, 0, 255), 3)
                M = cv2.moments(cnt)
                if Broc_Area > 5000:
                    X_broc = int(M['m10'] / M['m00'])
                    Y_broc = int(M['m01'] / M['m00'])
                    cv2.circle(frame, (X_broc, Y_broc), 10, (0, 0, 255), -1)
                    Real_X = int((640 - X_broc) / 5.783 + 845)
                    Real_Y = int(5 - ((480 - Y_broc) / 2.237))


            if(Broc_Area < 5000 and Stam_Area > Broc_Area):
                if X_stam < 450 and X_stam > 150:
                    print("ondersteboven")
                    if(time.time() - TimeBrocDetected > 0.5):
                        print("STAMX", Real_StamX)
                        print("STAMY", Real_StamY)
                        X_brocs.append(Real_StamX)
                        Y_brocs.append(Real_StamY)
                        Alpha_brocs.append(0)
                        TimeStamp = time.time()
                        Time_brocs.append(TimeStamp)
                        TimeBrocDetected = TimeStamp
                        print("ADDED UP SIDE DOWN")
                        print(Real_StamX, "::", Real_StamY, "::", TimeStamp)
        if Y_broc != 0  and X_broc < 450 and X_broc > 150:
            #print("BINNEN RANGE")
            if Y_brocs:
                if abs((Y_brocs[0] - Real_Y) > 5) or (time.time() - TimeBrocDetected > 0.5) :
                   #print("ADDING NA EERSTE")
                    print(Y_brocs[0])
                    X_brocs.append(Real_X)
                    Y_brocs.append(Real_Y)
                    Alpha_brocs.append(CalculateAngle())
                    TimeStamp = time.time()
                    Time_brocs.append(TimeStamp)
                    TimeBrocDetected = TimeStamp
                    print(Real_X,"::",Real_Y,"::",TimeStamp,"::",X_broc)
                #else:
                    #print("Y same")
            else:
               # print("ADDING")
                X_brocs.append(Real_X)
                Y_brocs.append(Real_Y)
                Alpha_brocs.append(CalculateAngle())
                TimeStamp = time.time()
                Time_brocs.append(TimeStamp)
                TimeBrocDetected = TimeStamp
                print(Real_X, "::", Real_Y, "::", TimeStamp,"::",X_broc)

        #cv2.imshow('fgbg_broc', mask_broc)
        #cv2.imshow('res_broc', res_broc)
        cv2.imshow('Original_ broc', frame)
        k = cv2.waitKey(30)

def StamVision():
    global X_stam, Y_stam, Real_StamX, Real_StamY, Stam_Area

    while True:
        frame = GetCameraImage()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV, 0)
        hsv = cv2.medianBlur(hsv, 11)

        lower_red_stam = np.array([0, 0, 201])
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
            Stam_Area = cv2.contourArea(cnt)
            print ("Area ", Stam_Area)
            if Stam_Area > 3000:
                cv2.drawContours(frame, contours_stam, -1, (0, 255, 255), 3)
                M = cv2.moments(cnt)
                if Stam_Area > 3000:
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    X_stam = int(M['m10'] / M['m00'])
                    Y_stam = int(M['m01'] / M['m00'])
                    Real_StamX = int((640 - X_stam) / 5.783 + 845)
                    Real_StamY = int(5 - ((480 - Y_stam) / 2.237))
                    print("X_stam: ", X_stam, " -> ", Real_StamX)
                    print("y_stam: ", Y_stam, " -> ", Real_StamY)
                    cv2.circle(frame, (X_stam, Y_stam), 10, (0, 0, 255), -1)

        #cv2.imshow('fgbg_stam', mask_stam)
        #cv2.imshow('res', res_stam)
        cv2.imshow('Original_ stam', frame)
        k = cv2.waitKey(30)

def CalculateAngle():
    global Real_X, Real_Y, Real_StamY, Real_StamX
    DeltaY = 0
    DeltaX = 0
    Alpha = 0
    ReturnAlpha = 1
    if (Real_X < Real_StamX):
        DeltaX = Real_StamX - Real_X
    else:
        DeltaX = Real_X - Real_StamX

    if (Real_StamY > Real_Y):
        DeltaY = Real_StamY - Real_Y
    else:
        DeltaY = Real_Y - Real_StamY

    if (DeltaX != 0 and DeltaY != 0):
        Alpha = int((math.atan(DeltaY / DeltaX) * 180) / 3.1415)
        # print("DeltaX ", DeltaX)
        # print("DeltaY ", DeltaY)
        print("Alpha",Alpha)
        if (Alpha > 65):
            ReturnAlpha = 0

    return ReturnAlpha

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
                DeleteBroc(0)
                ReadyToWrite = 1
                print ('ready received')
                received = ''


if __name__=="__main__":
    main()