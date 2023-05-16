import cv2
from command_line_parser import parser
import numpy as np


def init() -> None:
    global INPUT_PATH, OUTPUT_PATH, WIDTH, HEIGHT, IMAGE, WINDOW_NAME, ORIG_IMAGE, MARKERLIST, transformed

    args = parser.parse_args()

    INPUT_PATH = args.input.name
    OUTPUT_PATH = args.output
    WIDTH = args.width
    HEIGHT = args.height

    args.input.close()

    IMAGE = cv2.imread(INPUT_PATH)
    ORIG_IMAGE = IMAGE.copy()

    WINDOW_NAME = 'Preview Window'

    MARKERLIST = []

    transformed = False

    cv2.namedWindow(WINDOW_NAME)

    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)


def transform() -> None:
    global transformed

    points = np.float32(np.array(MARKERLIST))
    print(f'Points: {points}')
    destination = np.float32(
        np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]]))
    matrix = cv2.getPerspectiveTransform(points, destination)
    img_transformed = cv2.warpPerspective(
        ORIG_IMAGE.copy(), matrix, (WIDTH, HEIGHT), flags=cv2.INTER_LINEAR)
    cv2.imshow(WINDOW_NAME, cv2.flip(img_transformed, 0))
    transformed = True


def place_marker(x_pos: int, y_pos: int) -> None:
    global IMAGE, MARKERLIST

    IMAGE = cv2.circle(IMAGE, (x_pos, y_pos), 5, (255, 0, 0), -1)
    MARKERLIST.append([x_pos, y_pos])
    cv2.imshow(WINDOW_NAME, IMAGE)
    if len(MARKERLIST) == 4:
        transform()


def reset_canvas() -> None:
    global IMAGE, MARKERLIST, transformed
    MARKERLIST.clear()
    IMAGE = ORIG_IMAGE.copy()
    cv2.imshow(WINDOW_NAME, IMAGE)
    transformed = False


def mouse_callback(event: int, x: int, y: int, flags, param) -> None:
    if event == cv2.EVENT_LBUTTONDOWN and not transformed:
        place_marker(x, y)


if __name__ == '__main__':
    init()

    cv2.imshow(WINDOW_NAME, IMAGE)

    # https://stackoverflow.com/questions/35003476/opencv-python-how-to-detect-if-a-window-is-closed/37881722#37881722
    while cv2.getWindowProperty(WINDOW_NAME, 0) == 0:
        button = cv2.waitKey(0)

        if button == 27:
            reset_canvas()
        if button == ord('s') and transformed:
            print("Saving image...")
        if button == ord('q'):
            break
