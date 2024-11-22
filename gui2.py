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

    def draw_points(self, blended_image):
        if len(self.measurePoints) == 2:
            cv2.line(blended_image, self.measurePoints[0], self.measurePoints[1], BLUE_COLOR, 3)
        for point in self.measurePoints:
            cv2.circle(blended_image, point, 2, RED_COLOR, -1)
        return blended_image

    def show(self, rgb_image, depth_image, dst):
        # Преобразование карты глубины в цветовую карту
        # depth_image_norm = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint16)
        # depth_colormap = cv2.applyColorMap(depth_image_norm, cv2.COLORMAP_JET)
        
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.2), cv2.COLORMAP_JET)


        # Применение фильтрации для уменьшения шума
        depth_colormap = cv2.GaussianBlur(depth_colormap, (5, 5), 0)

        # Наложение карты глубины на цветное изображение с использованием альфа-канала
        alpha = 0.2  # Прозрачность карты глубины
        beta = 1 - alpha  # Прозрачность цветного изображения
        blended_image = cv2.addWeighted(rgb_image, beta, depth_colormap, alpha, 0)

        # Рисование точек и линий на смешанном изображении
        blended_image = self.draw_points(blended_image)

        # Вывод расстояния на смешанном изображении
        cv2.putText(blended_image, f"{dst} mm", [30, 30], cv2.FONT_HERSHEY_SIMPLEX, 1.2, WHITE_COLOR, 2)

        # Отображение смешанного изображения
        cv2.imshow(self.WINDOW_NAME, blended_image)

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
        window.show(image, np.zeros_like(image), 0)


if __name__ == '__main__':
    main()