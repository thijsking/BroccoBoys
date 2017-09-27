import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cv2.ocl.setUseOpenCL(False)
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
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
        cnt = contours[0]
        area = cv2.contourArea(cnt)
        if area > 0:
            cv2.drawContours(frame, contours, -1, (0, 255, 255), 3)
            M = cv2.moments(cnt)
            if area > 50:
                #hull = cv2.convexHull(cnt)
                #epsilon = 0.1 * cv2.arcLength(cnt, True)
                #approx = cv2.approxPolyDP(cnt, epsilon, True)
                #cv2.drawContours(frame,[approx],0,(0,0,255),2)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
                print("x=", cx, "y=", cy)
                array = [cx, cy]

    cv2.imshow('Original', frame)
    cv2.imshow('fgbg', mask)
    cv2.imshow('res', res)

    k = cv2.waitKey(30)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()