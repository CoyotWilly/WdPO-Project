import json
from pathlib import Path
from typing import Dict

import click
import cv2
from tqdm import tqdm
import numpy as np


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
    #TODO: Implement detection method.
    # (hMin = 23 , sMin = 36, vMin = 63), (hMax = 179 , sMax = 255, vMax = 255)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    
    red = 0
    yellow = 0
    green = 0
    purple = 0

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lb = np.array([23, 36, 63], np.uint8)
    ub = np.array([179, 255, 255], np.uint8)

    mask = cv2.inRange(hsv, lb, ub)

    blure = cv2.GaussianBlur(mask, (3, 3), 0)
    eges = cv2.Canny(blure, 10, 100)
    # eges = cv2.bilateralFilter(eges, 9, 75, 75)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilatet = cv2.dilate(eges, kernel, iterations=1)

    # contours
    contours, _ = cv2.findContours(dilatet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img2 = img.copy()
    cv2.drawContours(img2, contours, -1, (0, 255, 0), 2)
    print(len(contours))
    #
    cv2.imshow('Image', img2)
    cv2.imshow('Orginal', img)
    cv2.imshow('dilitate', eges)
    cv2.waitKey()
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
    # main()
    detect('data/25.jpg')
