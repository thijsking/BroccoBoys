import cv2
import numpy as np
import math
import socket

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = frame[150:380,0:450]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV, 0)

    lower_red_stam = np.array([21, 51, 105])
    upper_red_stam = np.array([51, 168, 255])

    mask_stam = cv2.inRange(hsv, lower_red_stam, upper_red_stam)
    res_stam = cv2.bitwise_and(frame, frame, mask=mask_stam)

    kernel = np.ones((5, 5), np.uint8)
    mask_stam = cv2.dilate(mask_stam, kernel, iterations=1)
    mask_stam = cv2.erode(mask_stam, kernel, iterations=3)
    mask_stam = cv2.dilate(mask_stam, kernel, iterations=5)
    #mask = cv2.erode(mask, kernel, iterations=4)
    #mask = cv2.dilate(mask, kernel, iterations=5)

    lower_red_broc = np.array([35, 17, 0])
    upper_red_broc = np.array([87, 255, 255])

    mask_broc = cv2.inRange(hsv, lower_red_broc, upper_red_broc)
    res = cv2.bitwise_and(frame, frame, mask=mask_broc)

    kernel = np.ones((5, 5), np.uint8)
    mask_broc = cv2.dilate(mask_broc, kernel, iterations=1)
    mask_broc = cv2.erode(mask_broc, kernel, iterations=3)
    mask_broc = cv2.dilate(mask_broc, kernel, iterations=2)
    mask_broc = cv2.erode(mask_broc, kernel, iterations=4)
    mask_broc = cv2.dilate(mask_broc, kernel, iterations=5)

    X_stam = 0
    Y_stam = 0
    X_broc = 0
    Y_broc = 0
    DeltaX = 0
    DeltaY = 0
    _, contours_stam, hierarchy = cv2.findContours(mask_stam, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_stam:
        # print('contouyrs')
        cnt = contours_stam[0]
        area = cv2.contourArea(cnt)
        if area > 0:
            cv2.drawContours(frame, contours_stam, -1, (0, 255, 255), 3)
            M = cv2.moments(cnt)
            if area > 50:
                # print('grote area')
                # hull = cv2.convexHull(cnt)
                # epsilon = 0.1 * cv2.arcLength(cnt, True)
                # approx = cv2.approxPolyDP(cnt, epsilon, True)
                # cv2.drawContours(frame,[approx],0,(0,0,255),2)
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                X_stam = int(M['m10'] / M['m00'])
                Y_stam = int(M['m01'] / M['m00'])
                cv2.circle(frame, (X_stam, Y_stam), 10, (0, 0, 255), -1)
                #ellipse = cv2.fitEllipse(cnt)
                #cv2.ellipse(frame, ellipse, (0, 255, 0), 2)
                #rows, cols = img.shape[:2]
                #[vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
                #lefty = int((-x * vy / vx) + y)
                #righty = int(((cols - x) * vy / vx) + y)
                #cv2.line(frame, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)

        _, contours_broc, hierarchy = cv2.findContours(mask_broc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours_broc:
            # print('contouyrs')
            cnt = contours_broc[0]
            area = cv2.contourArea(cnt)
            if area > 0:
                cv2.drawContours(frame, contours_broc, -1, (0, 255, 255), 3)
                M = cv2.moments(cnt)
                if area > 500:
                    # print('grote area')
                    # hull = cv2.convexHull(cnt)
                    # epsilon = 0.1 * cv2.arcLength(cnt, True)
                    # approx = cv2.approxPolyDP(cnt, epsilon, True)
                    # cv2.drawContours(frame,[approx],0,(0,0,255),2)
                    X_broc = int(M['m10'] / M['m00'])
                    Y_broc = int(M['m01'] / M['m00'])
                    cv2.circle(frame, (X_broc, Y_broc), 10, (0, 0, 255), -1)
                    # print("x=", cx, "y=", cy)
                    # array = [cx, cy]
                    # rx = int(cx * -2.1 + 1017.4)
                    # if rx > 565:
                    #     rx = 565
                    # if rx < 130:
                    #     rx = 130

    if(X_stam > X_broc):
        deltaX = X_stam - X_broc
    else:
        deltaX = X_broc - X_broc
    if (Y_stam > Y_broc):
        deltaY = Y_stam - Y_broc
    else:
        deltaX = Y_broc - Y_broc

    Alpha = math.atan(deltaY/deltaX)


    cv2.imshow('Original', frame)
    cv2.imshow('fgbg_stam', mask_stam)
    cv2.imshow('res', res_stam)



    k = cv2.waitKey(30)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()