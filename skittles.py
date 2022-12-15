import json
import cv2
import numpy as np

# VALUES FOR FUTURE IMPLEMENTATION
# purple tres setup
# aggressive_purple = [(71, 95, 0), (179, 255, 255)]
# normal_purple = [(151, 36, 0), (179, 255, 255)]
#
# green tres setup
# aggressive_yellow = [(35, 189, 0), (69, 255, 255)]
# normal_yellow = [(35, 82, 0), (69, 255, 255)]
#
# yellow tres setup
# aggressive_green = [(0, 220, 116), (32, 255, 255)]
# normal_green = [(0, 137, 102), (30, 255, 255)]
#
# red tres setup
# aggressive_red = [(170, 102, 153), (179, 255, 255)]
# normal_red = [(175, 46, 0), (179, 255, 255)]


def count_cnts(cnts):
    # GREEN % val = 0.00005
    area_array = np.array([0])
    shape = np.shape(img)
    condition = (shape[0] * shape[1]) * 0.00005
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > condition:
            area_array = np.append(area_array, area)
    area_array = np.delete(area_array, 0)
    return area_array


def color_count_check(area_arr, counted):
    std = np.std(area_arr)
    avg = np.average(area_arr)
    lb = np.abs(avg - std)
    ub = avg + std
    # print('lb=', lb)
    # print('ub=', ub)

    for field in area_arr:
        if field < lb and counted > 0:
            counted = counted - 1
        elif field > ub:
            counted = counted + 1
    return counted


def green_count():
    blur = 0

    # blur-ing process
    for i in range(5):
        blur = cv2.medianBlur(hsv, 11)

    # morphology
    mask_g = cv2.inRange(blur, (35, 189, 0), (69, 255, 190))
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (12, 12))
    mask_close_g = cv2.morphologyEx(mask_g, cv2.MORPH_CLOSE, ker)
    mask_open_g = cv2. morphologyEx(mask_close_g, cv2.MORPH_OPEN, ker)

    # object counting
    ker_g = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    dilatet = cv2.dilate(mask_open_g, ker_g, iterations=1)

    cnt_g, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # final result display and human check
    # counted = len(cnt_g)
    counted = len(count_cnts(cnt_g))
    # print('Counted=', counted)

    g_mask_final = cv2.cvtColor(mask_open_g, cv2.COLOR_GRAY2BGR)
    g_final = cv2.addWeighted(g_mask_final, 0.5, img, 0.5, 0)


    # cv2.imshow('close mask', g_final)
    # cv2.imwrite('test.jpg', g_final)
    # cv2.waitKey(0)
    return counted

def yellow_count():
    blur = 0
    for i in range(5):
        blur = cv2.medianBlur(hsv, 11)

    # morphology
    mask_y = cv2.inRange(blur, (0, 220, 116), (32, 255, 255))
    ker_y_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    ker_y_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask_close_y = cv2.morphologyEx(mask_y, cv2.MORPH_CLOSE, ker_y_close)
    mask_open_y = cv2.morphologyEx(mask_close_y, cv2.MORPH_OPEN, ker_y_open)
    # cv2.imshow('maks', mask_open_y)

    # object counting
    ker_y = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    dilatet = cv2.dilate(mask_open_y, ker_y, iterations=1)

    cnt_y, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # final result display and human check
    counted = len(count_cnts(cnt_y))
    # print('Counted=', counted)
    y_mask_final = cv2.cvtColor(mask_open_y, cv2.COLOR_GRAY2BGR)
    y_final = cv2.addWeighted(y_mask_final, 0.5, img, 0.5, 0)

    # cv2.imshow('close mask', y_final)
    # cv2.imwrite('test.jpg', y_final)
    # cv2.waitKey(0)
    return counted

def red_count():
    blur = hsv
    for i in range(5):
        blur = cv2.medianBlur(blur, 11)

    # morphology
    mask_r = cv2.inRange(blur, (170, 102, 153), (179, 255, 255))
    # ker (10, 10) AND ker(3, 3)
    # mask_r = cv2.inRange(blur, (170, 135, 100), (179, 255, 255))
    ker_r = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask_close_r = cv2.morphologyEx(mask_r, cv2.MORPH_CLOSE, ker_r)
    mask_open_r = cv2.morphologyEx(mask_close_r, cv2.MORPH_OPEN, ker_r)
    # cv2.imshow('maks', mask_open_r)

    # object counting
    ker_r = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    dilatet = cv2.dilate(mask_open_r, ker_r, iterations=1)

    cnt_r, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # final result display and human check
    counted = len(count_cnts(cnt_r))
    # print('Counted=', counted)
    # r_mask_final = cv2.cvtColor(mask_open_r, cv2.COLOR_GRAY2BGR)
    # r_final = cv2.addWeighted(r_mask_final, 0.5, img, 0.5, 0)

    # cv2.imshow('close mask', r_final)
    # cv2.imwrite('test.jpg', r_mask_final)
    # cv2.waitKey(0)
    return counted


def purple_count():
    blur = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    for i in range(5):
        blur = cv2.medianBlur(blur, 11)
    # mask_p = cv2.inRange(blur, (0, 127, 120), (108, 132, 140))
    # morphology
    # mask_p = cv2.inRange(blur, (71, 95, 0), (179, 255, 255))
    mask_p = cv2.inRange(blur, (160, 85, 0), (168, 185, 255))
    # ker_p = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    # mask_close_p = cv2.morphologyEx(mask_p, cv2.MORPH_CLOSE, (1, 1))
    # mask_open_p = cv2.morphologyEx(mask_close_p, cv2.MORPH_OPEN, (10, 10))
    # cv2.imshow('maks', mask_open_p)

    # object counting

    ker_p = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    dilatet = cv2.dilate(mask_p, ker_p, iterations=1)

    cnt_p, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # final result display and human check
    counted = len(count_cnts(cnt_p))
    # counted = len(cnt_p)
    print('Counted=', counted)
    p_mask_final = cv2.cvtColor(mask_p, cv2.COLOR_GRAY2BGR)
    p_final = cv2.addWeighted(p_mask_final, 0.5, img, 0.5, 0)

    cv2.imshow('final', p_final)
    # cv2.imwrite('test.jpg', p_final)
    cv2.waitKey(0)
    return counted


def call_counting():
    # GREEN 97.5%
    # YELLOW 97.5%
    # RED 95%
    # PURPLE %
    green_count()
    yellow_count()
    red_count()
    purple_count()


if __name__ == '__main__':
    # pic 20 17 32
    img = cv2.imread('data/00.jpg', cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    purple_count()
    # file = open('the_truth.json')
    # data = json.load(file)
    # val = 0
    # sum = 0
    # for i in range(39):
    #     if i < 10:
    #         img_path = "data/0" + str(i) + ".jpg"
    #         val = "0"+ str(i) + ".jpg"
    #     else:
    #         img_path = "data/" + str(i) + ".jpg"
    #         val = str(i) + ".jpg"
    #     img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    #     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #     perfect = data[val]["purple"]
    #     return_val = purple_count()
    #     sum = sum + np.abs(perfect - return_val)
    #     if return_val != perfect:
    #         print('blad na zdjeciu '+ str(i))
    # print(sum)
