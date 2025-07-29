from dataclasses import dataclass
import cv2
from cv2.typing import MatLike
from os.path import isfile, exists
from os import get_terminal_size
import numpy as np

LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"


@dataclass
class Video:
    path: str

    def play_video(self):
        if not exists(self.path) or not isfile(self.path):
            raise Exception(f"File doesn't exist or is a directory.")
        self.vid = cv2.VideoCapture(self.path)

        if not self.vid.isOpened():
            raise Exception(f"File couldn't be opened.")

        width = get_terminal_size(0)[0]
        height = get_terminal_size(0)[1] - 1  # account for new line
        while self.vid.isOpened():
            _, frame = self.vid.read()
            if not frame.any():
                break
            resized: MatLike = self.resize(frame, width, height)
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
