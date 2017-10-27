import cv2
import numpy as np

cap = cv2.VideoCapture(1)
def nothing(x):
    pass

cv2.namedWindow('wheel')

cv2.createTrackbar('H-lower', 'wheel', 0, 255, nothing)
cv2.createTrackbar('S-lower', 'wheel', 0, 255, nothing)
cv2.createTrackbar('V-lower', 'wheel', 0, 255, nothing)
cv2.createTrackbar('H-upper', 'wheel', 0, 255, nothing)
cv2.createTrackbar('S-upper', 'wheel', 0, 255, nothing)
cv2.createTrackbar('V-upper', 'wheel', 0, 255, nothing)

while True:
    _, frame = cap.read()
    #frame = frame[150:380, 0:450]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.medianBlur(hsv,11)


    hLow = cv2.getTrackbarPos('H-lower', 'wheel')
    sLow = cv2.getTrackbarPos('S-lower', 'wheel')
    vLow = cv2.getTrackbarPos('V-lower', 'wheel')
    hHigh = cv2.getTrackbarPos('H-upper', 'wheel')
    sHigh = cv2.getTrackbarPos('S-upper', 'wheel')
    vHigh = cv2.getTrackbarPos('V-upper', 'wheel')

    lower_green = np.array([hLow, sLow, vLow])
    upper_green = np.array([hHigh, sHigh, vHigh])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(hsv, frame, mask=mask)


    cv2.imshow('Original', hsv)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    k = cv2.waitKey(30)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()