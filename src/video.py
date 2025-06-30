import cv2
from cv2.typing import MatLike
from os.path import isfile, exists
import numpy as np


class Video:
    path: str
    vid: cv2.VideoCapture

    def __init__(self):
        pass

    def load_video(self, path: str):
        if not exists(path) or not isfile(path):
            raise Exception("File doesn't exist or is a directory")
        self.vid = cv2.VideoCapture(path)
        if not self.vid.isOpened():
            raise Exception("File couldn't be opened")
        count = 0
        while self.vid.isOpened():
            ret, frame = self.vid.read()
            count += 1
            if count > 500:
                print(self.to_ascii(frame))
                resized = self.resize(frame, 640, 480)
                cv2.imwrite("TestFrame.jpg", resized)
                break
        self.vid.release()

    def resize(self, frame: MatLike, width: int, height: int) -> MatLike:
        width_ratio: float = width / frame.shape[1]
        height_ratio: float = height / frame.shape[0]
        new_w = int(frame.shape[1] * width_ratio)
        new_h = int(frame.shape[0] * height_ratio)
        return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    def to_ascii(self, frame: MatLike):
        ascii_chars = "@%#*+=-:. "
        height = frame.shape[0]
        width = frame.shape[1]
        b, g, r = cv2.split(frame)
        per_pixel_brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
        out = []
        for i in range(height):
            for j in range(width):
                brightness = per_pixel_brightness[i][j]
                out[i][j] = ascii_chars[brightness % 10]
            out[i][width] = "\n"
        print(out[100][100])


v = Video()
v.load_video("videos/test.mp4")
