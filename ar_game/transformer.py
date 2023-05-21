"""
This module returns transformed frames from the webcam

Frames are warped in perspective
"""
import cv2 as cv
import numpy as np
from PIL import Image
import cv2.aruco as aruco
from imutils import perspective
import pyglet

class Transformer:
    def __init__(self, capture_channel: int):
        """
        Initializes webcam capture

        Args:
            capture_channel: source of webcam feed
        """
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        self.aruco_params = aruco.DetectorParameters()

        self.cap = cv.VideoCapture(capture_channel)
        self.WINDOW_WIDTH = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.WINDOW_HEIGHT = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    def get_transformed_image(self):
        """
        Performs warp perspective transformation on webcam frame

        Returns:
            transformed frame in pyglet.image.ImageData format

            None if less than 4 AruCo markers are detected
        """
        ret, frame = self.cap.read()

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)

        if ids is not None and len(ids) == 4:
            points = []
            for marker in corners:
                points.append(marker[0][2].tolist())
            points = perspective.order_points(np.array(points))
            destination = np.float32(
                np.array([[0, 0], [self.WINDOW_WIDTH, 0], [self.WINDOW_WIDTH, self.WINDOW_HEIGHT], [0, self.WINDOW_HEIGHT]]))
            matrix = cv.getPerspectiveTransform(points, destination)
            frame = cv.warpPerspective(
            frame, matrix, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), flags=cv.INTER_LINEAR)

            frame = cv.flip(frame, 1)

            rows, cols, channels = frame.shape

            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            raw_img = Image.fromarray(rgb_frame).tobytes()

            top_to_bottom_flag = -1
            bytes_per_row = channels*cols
            pyimg = pyglet.image.ImageData(width=cols, 
                                            height=rows, 
                                            fmt='RGB', 
                                            data=raw_img, 
                                            pitch=top_to_bottom_flag*bytes_per_row)
            return pyimg
        else:
            return None

    def get_finger_position(self, canvas_state):
        """
        Detects finger position on canvas.

        Detection works by converting image to gray and using an adaptive threshold to detect finger shape

        Returns:
            np.array[][] with size of webcam frame, '0' for finger position '255' for empty space
        """
        canvas_state_cv = np.array(Image.frombytes('RGB', (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), canvas_state))

        canvas_state_grey = cv.cvtColor(canvas_state_cv, cv.COLOR_RGB2GRAY)

        adaptive = cv.adaptiveThreshold(canvas_state_grey, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)

        _, canvas_state_thresh = cv.threshold(canvas_state_grey, 110, 255, cv.THRESH_BINARY)

        canvas_state_thresh = np.flip(canvas_state_thresh, 0)

        return canvas_state_thresh
