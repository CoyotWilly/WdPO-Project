import cv2
import numpy as np


def count_obj(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilatet = cv2.dilate(img, kernel, iterations=1)

    # contours
    contours, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    print(len(contours))
    cv2.imshow('counter call', img)


# (hMin = 23 , sMin = 36, vMin = 63), (hMax = 179 , sMax = 255, vMax = 255)
img_path = 'data/01.jpg'
img = cv2.imread(img_path, cv2.IMREAD_COLOR)
img = cv2.resize(img, (768, 1020))

grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(grey, (3, 3), 0)

t_inv = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 4)
canny = cv2.Canny(t_inv, 100, 200)
mask = cv2.bitwise_and(img, img, mask=canny)

count_obj(mask)

cv2.imshow('mask', mask)
cv2.imshow('testy', canny)
cv2.waitKey()

