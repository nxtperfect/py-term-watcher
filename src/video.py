import cv2
from cv2.typing import MatLike
from os.path import isfile, exists
import numpy as np

LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"


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

        while self.vid.isOpened():
            ret, frame = self.vid.read()
            if not frame.any():
                break
            resized: MatLike = self.resize(frame, 640 / 4, 480 / 11)
            grayscale: MatLike = self.grayscale(resized)
            ascii_frame: list[list[str]] = self.grayscale_to_ascii(grayscale)
            for line in ascii_frame:
                print("".join(line))
            for _ in range(len(ascii_frame)):
                print(LINE_UP, end=LINE_CLEAR)
        self.vid.release()

    def resize(self, frame: MatLike, width: int, height: int) -> MatLike:
        width_ratio: float = width / frame.shape[1]
        height_ratio: float = height / frame.shape[0]
        new_w = int(frame.shape[1] * width_ratio)
        new_h = int(frame.shape[0] * height_ratio)
        return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    def grayscale(self, frame: MatLike) -> MatLike:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def grayscale_to_ascii(self, frame: MatLike) -> list[list[str]]:
        ascii_chars = (
            """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`'."""
        )
        height: int = frame.shape[0]
        width: int = frame.shape[1]
        per_pixel_brightness: MatLike = cv2.split(frame)[0]
        frame_ascii = np.zeros(shape=(height, width), dtype=str)
        for i in range(height):
            for j in range(width):
                brightness: int = round(
                    (per_pixel_brightness[i][j] / 255) * len(ascii_chars) - 1
                )
                frame_ascii[i][j] = ascii_chars[brightness]
        return frame_ascii


v = Video()
v.load_video("videos/test.mp4")
