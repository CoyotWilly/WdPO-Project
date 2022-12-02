import numpy as np
import cv2

# VALUES FOR FUTURE IMPLEMENTATION
# purple tres setup
# aggressive_purple = [(71, 95, 0), (179, 255, 255)]
# normal_purple = [(151, 36, 0), (179, 255, 255)]
#
# yellow tres setup
# aggressive_yellow = [(35, 189, 0), (69, 255, 255)]
# normal_yellow = [(35, 82, 0), (69, 255, 255)]
#
# green tres setup
# aggressive_green = [(0, 220, 116), (32, 255, 255)]
# normal_green = [(0, 137, 102), (30, 255, 255)]
#
# red tres setup
# aggressive_red = [(170, 102, 153), (179, 255, 255)]
# normal_red = [(175, 46, 0), (179, 255, 255)]
#
# DONT TOUCH IT:
red = 0
yellow = 0
green = 0
purple = 0


img = cv2.imread('data/00.jpg', cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
blur = 0

# blur-ing process
for i in range(5):
    blur = cv2.medianBlur(hsv, 11)

mask_y = cv2.inRange(blur, (35, 189, 0), (69, 255, 255))
ker_y = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (12, 12))
mask_close_y = cv2.morphologyEx(mask_y, cv2.MORPH_CLOSE, ker_y)
mask_open_y = cv2. morphologyEx(mask_close_y, cv2.MORPH_OPEN, ker_y)

ker_y = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dilatet = cv2.dilate(mask_open_y, ker_y, iterations=2)
#
cnt_y, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(cnt_y)):
    if len(cnt_y[i]) > 160:
        yellow = yellow + 1
print('yellow=', yellow)
print('Counted=', len(cnt_y))

y_mask_final = cv2.cvtColor(mask_open_y, cv2.COLOR_GRAY2BGR)
y_final = cv2. addWeighted(y_mask_final, 0.5, img, 0.5, 0)

# cv2.imshow('close mask', y_final)
cv2.waitKey(0)