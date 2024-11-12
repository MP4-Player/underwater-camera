import cv2
import numpy as np

from utils import *


class CvWindow(object):

    WINDOW_NAME = "Underwater Meter"

    def __init__(self):
        self.measurePoints = []
        cv2.namedWindow(self.WINDOW_NAME)
        cv2.setMouseCallback(self.WINDOW_NAME, self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.measurePoints) == 2:
                self.measurePoints.clear()
            self.measurePoints.append([x, y])

    def draw_points(self, rgb_image):
        if len(self.measurePoints) == 2:
            cv2.line(rgb_image, self.measurePoints[0], self.measurePoints[1], BLUE_COLOR, 3)
        for point in self.measurePoints:
            cv2.circle(rgb_image, point, 5, RED_COLOR, -1)
        return rgb_image

    def show(self, rgb_image, dst):
        rgb_image[:40, :] = 0
        rgb_image = self.draw_points(rgb_image)
        cv2.putText(rgb_image, f"{dst} mm", [30, 30], cv2.FONT_HERSHEY_SIMPLEX, 1.2, WHITE_COLOR, 2)
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
        cv2.imshow(self.WINDOW_NAME, bgr_image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            cv2.destroyWindow(self.WINDOW_NAME)
            exit()


def main():
    window = CvWindow()
    while True:
        image = np.zeros([480, 640], np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        cv2.putText(image, "TEST IMAGE", [200, 240], cv2.FONT_HERSHEY_SIMPLEX, 1.2, WHITE_COLOR, 2)
        window.show(image, 0)


if __name__ == '__main__':
    main()
