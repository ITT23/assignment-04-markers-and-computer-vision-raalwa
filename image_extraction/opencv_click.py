import cv2
from command_line_parser import parser
from pynput import keyboard

def handle_keyboard_event(key: keyboard.Key):
    if key == keyboard.Key.esc:
        print("ESC pressed")


def init() -> None:
    global INPUT_PATH, OUTPUT_PATH, WIDTH, HEIGHT, LISTENER, IMAGE

    args = parser.parse_args()

    INPUT_PATH = args.input.name
    OUTPUT_PATH = args.output
    WIDTH = args.width
    HEIGHT = args.height

    args.input.close()

    LISTENER = keyboard.Listener(on_release=handle_keyboard_event)
    IMAGE = cv2.imread(INPUT_PATH)

def place_marker(x_pos: int, y_pos: int):
    global IMAGE
    IMAGE = cv2.circle(IMAGE, (x_pos, y_pos), 5, (255, 0, 0), -1)
    cv2.imshow(WINDOW_NAME, IMAGE)

def reset_markers():
    pass

def mouse_callback(event: int, x: int, y: int, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        place_marker(x,y)


if __name__ == '__main__':
    init()

    WINDOW_NAME = 'Preview Window'

    cv2.namedWindow(WINDOW_NAME)

    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)
    cv2.imshow(WINDOW_NAME, IMAGE)

    # LISTENER.start()

    cv2.waitKey(-1)
