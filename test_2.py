import cv2
import numpy as np

def count_obj(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilatet = cv2.dilate(img, kernel, iterations=2)
    # contours
    contours, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    print(len(contours))
    cv2.imshow('counter call', img)


def get_u(img):
    tres = cv2.inRange(img, (159, 90, 0), (179, 255, 255))
    cnts, hiers = cv2.findContours(tres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    for cnt in cnts:
        ellipse = cv2.fitEllipse(cnt)
        cv2.ellipse(img, ellipse, (255, 0, 255), 1, cv2.LINE_AA)
    cv2.imshow('ellipse', img)


# blur = cv2.bilateralFilter(hsv, 9, 25, 10)
# ret, tres = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY_INV)
img = cv2.imread('data/00.jpg', cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
get_u(img)
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
# tres = cv2.inRange(hsv, (0, 0, 0.42 * 255), (255, 0.25 * 255, 255))
# morphology
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
# morph = cv2.morphologyEx(tres, cv2.MORPH_CLOSE, kernel)
# mask = (255 - tres)
# canny = cv2.Canny(mask, 100, 200)


# mask = cv2.bitwise_and(img, img, mask=mask)
#
# count_obj(canny)
# cv2.imshow('hvs mask', canny)
cv2.waitKey()