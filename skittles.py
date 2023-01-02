import json
import cv2
import numpy as np


def count_cnts(cnts: list, color_called: str) -> np.ndarray:
    area_array = np.array([0])
    shape = np.shape(img)
    if color_called == "purple":
        condition = (shape[0] * shape[1]) * 0.000075
    else:
        condition = (shape[0] * shape[1]) * 0.00005

    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area > condition:
            area_array = np.append(area_array, area)
    area_array = np.delete(area_array, 0)
    return area_array


def green_count():
    # blurring
    blur = cv2.medianBlur(hsv, 11)

    # morphology and dilation
    mask_g = cv2.inRange(blur, (35, 189, 0), (69, 255, 190))
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (12, 12))
    mask_close_g = cv2.morphologyEx(mask_g, cv2.MORPH_CLOSE, ker)
    mask_open_g = cv2. morphologyEx(mask_close_g, cv2.MORPH_OPEN, ker)
    ker_g = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    dilatet = cv2.dilate(mask_open_g, ker_g, iterations=1)

    # object counting
    cnt_g, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # final result calc
    counted = len(count_cnts(cnt_g, "green"))

    return counted

def yellow_count():
    blur = cv2.medianBlur(hsv, 11)

    # morphology and dilation
    mask_y = cv2.inRange(blur, (0, 220, 116), (32, 255, 255))
    ker_y_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    ker_y_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask_close_y = cv2.morphologyEx(mask_y, cv2.MORPH_CLOSE, ker_y_close)
    mask_open_y = cv2.morphologyEx(mask_close_y, cv2.MORPH_OPEN, ker_y_open)
    ker_y = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    dilatet = cv2.dilate(mask_open_y, ker_y, iterations=1)

    # object counting
    cnt_y, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # final result calc
    counted = len(count_cnts(cnt_y, "yellow"))

    return counted

def red_count():
    # blurring and threshold appliance
    blur = cv2.medianBlur(hsv, 11)
    mask_r = cv2.inRange(blur, (170, 102, 153), (179, 255, 255))

    # morphology and dilation
    ker_r = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask_close_r = cv2.morphologyEx(mask_r, cv2.MORPH_CLOSE, ker_r)
    mask_open_r = cv2.morphologyEx(mask_close_r, cv2.MORPH_OPEN, ker_r)
    ker_r = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    dilatet = cv2.dilate(mask_open_r, ker_r, iterations=1)

    # object counting
    cnt_r, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # final result calc
    counted = len(count_cnts(cnt_r, "red"))
    return counted


def purple_count():
    blur = cv2.medianBlur(hsv, 11)
    mask_range = cv2.inRange(blur, (160, 82, 0), (176, 234, 101))
    mask_dil = cv2.dilate(mask_range, (10,10))

    # object counting
    cnt, _ = cv2.findContours(mask_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # final result calc
    counted = len(count_cnts(cnt, "purple"))

    return counted


if __name__ == '__main__':
    file = open('the_truth.json')
    data = json.load(file)
    file.close()
    color = ["green", "yellow", "red", "purple"]
    func = [green_count, yellow_count, red_count, purple_count]
    val = sum_calc = 0

    for i in range(len(color)):
        print("Current color=" + color[i])
        for j in range(39):
            if j < 10:
                img_path = "data/0" + str(j) + ".jpg"
                val = "0"+ str(j) + ".jpg"
            else:
                img_path = "data/" + str(j) + ".jpg"
                val = str(j) + ".jpg"
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            perfect = data[val][color[i]]
            return_val = func[i]()
            sum_calc = sum_calc + np.abs(perfect - return_val)
            if return_val != perfect:
                print('blad na zdjeciu '+ str(j))
        print(sum_calc)


