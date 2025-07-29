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
                ascii_frame = self.to_ascii(frame)
                resized = self.resize(frame, 640, 480)
                grayscale = self.grayscale(resized)
                cv2.imwrite("TestFrame.jpg", resized)
                cv2.imwrite("TestFrameGrayscale.jpg", grayscale)
                break
        self.vid.release()

    def resize(self, frame: MatLike, width: int, height: int) -> MatLike:
        width_ratio: float = width / frame.shape[1]
        height_ratio: float = height / frame.shape[0]
        new_w = int(frame.shape[1] * width_ratio)
        new_h = int(frame.shape[0] * height_ratio)
        return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    def grayscale(self, frame: MatLike):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def to_ascii(self, frame: MatLike):
        ascii_chars = "@%#*+=-:. "
        height = frame.shape[0]
        width = frame.shape[1]
        b, g, r = cv2.split(frame)
        per_pixel_brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
        out = [[" "] * width] * height
        print(len(out), len(out[0]))
        for i in range(height - 1):
            for j in range(width - 2):
                brightness = per_pixel_brightness[i][j]
                out[i][j] = ascii_chars[int(brightness % 10)]
            out[i][width - 1] = "\n"
        print(out[100][100])
        print(["".join(x) for x in out])
        return out


v = Video()
v.load_video("videos/test.mp4")
