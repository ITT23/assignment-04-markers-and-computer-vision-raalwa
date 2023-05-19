"""
This module displays an image and allows for a warp perspective transformation.

The user selects four points on the canvas,
which are used to transform the image.
The transformed image can be saved by pressing "s".
All changes can be reset by pressing "Esc".
The application can be closed by pressing "q".

Execute with the following command-line arguments:
    python opencv_click.py input_destination output_destination output_width output_height
For detailed information use:
    python opencv_click.py --help|--h
"""
from typing import List

import cv2 as cv
import numpy as np
from command_line_parser import parser
from imutils import perspective


def init() -> None:
    """
    Retrieves command-line argumets and initializes Opencv.
    """
    global INPUT_PATH, OUTPUT_PATH, WIDTH,\
        HEIGHT, WINDOW_NAME, ORIG_IMAGE,\
        image, markerlist, transformed

    args = parser.parse_args()

    INPUT_PATH = args.input.name
    OUTPUT_PATH = args.output
    WIDTH = args.width
    HEIGHT = args.height

    args.input.close()

    image = cv.imread(INPUT_PATH)
    ORIG_IMAGE = image.copy()

    WINDOW_NAME = 'Preview Window'

    markerlist = []

    transformed = False

    cv.namedWindow(WINDOW_NAME)

    cv.setMouseCallback(WINDOW_NAME, mouse_callback)


def sort_markers(points: List[List[float]]) -> np.ndarray:
    """
    Orders points in list counterclockwise, starting from bottom left corner.

    This is needed to ensure the right orientation of the transformed image.

    Args:
        points: Unsorted list of four coordinates [x_position, y_position]

    Returns:
        Counterclockwise sorted list of point, starting from bottom left
    """
    pts = perspective.order_points(np.array(points))
    return pts


def transform() -> None:
    """
    Warps perspecive of image according to position of markers.
    """
    global transformed, image

    points = np.float32(sort_markers(markerlist))
    destination = np.float32(
        np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]]))
    matrix = cv.getPerspectiveTransform(points, destination)
    img_transformed = cv.warpPerspective(
        ORIG_IMAGE.copy(), matrix, (WIDTH, HEIGHT), flags=cv.INTER_LINEAR)
    image = img_transformed
    cv.imshow(WINDOW_NAME, image)
    transformed = True


def place_marker(x_pos: int, y_pos: int) -> None:
    """
    Handles display of markers and starts transformaiton if enough markers are placed.
    """
    global image, markerlist

    image = cv.circle(image, (x_pos, y_pos), 5, (255, 0, 0), -1)
    markerlist.append([x_pos, y_pos])
    cv.imshow(WINDOW_NAME, image)
    if len(markerlist) == 4:
        transform()


def reset_canvas() -> None:
    """
    Undoes every change to the image and displays original image.
    """
    global image, markerlist, transformed
    markerlist.clear()
    image = ORIG_IMAGE.copy()
    cv.imshow(WINDOW_NAME, image)
    transformed = False


def mouse_callback(event: int, x: int, y: int, flags, param) -> None:
    """
    Sets callback for left mouse button to place a marker.
    """
    if event == cv.EVENT_LBUTTONDOWN and not transformed:
        place_marker(x, y)


def save_image() -> None:
    """
    Saves transformed image to file specified in OUTPUT_PATH command-line argument.
    """
    cv.imwrite(OUTPUT_PATH, image)


if __name__ == '__main__':
    init()

    cv.imshow(WINDOW_NAME, image)

    # https://stackoverflow.com/questions/35003476/opencv-python-how-to-detect-if-a-window-is-closed/37881722#37881722
    while cv.getWindowProperty(WINDOW_NAME, 0) == 0:
        button = cv.waitKey(0)

        if button == 27:
            reset_canvas()
        if button == ord('s') and transformed:
            save_image()
            reset_canvas()
        if button == ord('q'):
            break
