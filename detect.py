import json
from pathlib import Path
from typing import Dict

import click
import cv2
from tqdm import tqdm
import numpy as np


def count_cnts(cnts: list, color_called: str, img: np.ndarray) -> np.ndarray:
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


def green_count(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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
    counted = len(count_cnts(cnt_g, "green", img))

    return counted

def yellow_count(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # blurring
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
    counted = len(count_cnts(cnt_y, "yellow", img))

    return counted

def red_count(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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
    counted = len(count_cnts(cnt_r, "red", img))
    return counted


def purple_count(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # blurring and threshold appliance
    blur = cv2.medianBlur(hsv, 11)

    # dilation
    mask_range = cv2.inRange(blur, (160, 82, 0), (176, 234, 101))
    mask_dil = cv2.dilate(mask_range, (10,10))

    # object counting
    cnt, _ = cv2.findContours(mask_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # final result calc
    counted = len(count_cnts(cnt, "purple", img))

    return counted

def detect(img_path: str) -> Dict[str, int]:
    """Object detection function, according to the project description, to implement.
    Parameters
    ----------
    img_path : str
        Path to processed image.
    Returns
    -------
    Dict[str, int]
        Dictionary with quantity of each object.
    """
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    red = red_count(img)
    yellow = yellow_count(img)
    green = green_count(img)
    purple = purple_count(img)

    return {'red': red, 'yellow': yellow, 'green': green, 'purple': purple}


@click.command()
@click.option('-p', '--data_path', help='Path to data directory', type=click.Path(exists=True, file_okay=False, path_type=Path), required=True)
@click.option('-o', '--output_file_path', help='Path to output file', type=click.Path(dir_okay=False, path_type=Path), required=True)
def main(data_path: Path, output_file_path: Path):
    img_list = data_path.glob('*.jpg')

    results = {}

    for img_path in tqdm(sorted(img_list)):
        fruits = detect(str(img_path))
        results[img_path.name] = fruits

    with open(output_file_path, 'w') as ofp:
        json.dump(results, ofp)


if __name__ == '__main__':
    main()
