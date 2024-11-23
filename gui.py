import cv2
import numpy as np
from utils import *

def show(rgb_image, depth_image):
        
        # Преобразование карты глубины в цветовую карту
        # depth_image_norm = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint16)
        # depth_colormap = cv2.applyColorMap(depth_image_norm, cv2.COLORMAP_JET)
        
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.2), cv2.COLORMAP_INFERNO)


        # Применение фильтрации для уменьшения шума
        depth_colormap = cv2.GaussianBlur(depth_colormap, (5, 5), 0)

        # Наложение карты глубины на цветное изображение с использованием альфа-канала
        alpha = 0.3 # Прозрачность карты глубины
        beta = 1 - alpha  # Прозрачность цветного изображения
        blended_image = cv2.addWeighted(rgb_image, beta, depth_colormap, alpha, 0)
        # blended_image = self.draw_points(blended_image)

        # Вывод расстояния на смешанном изображении
        # cv2.putText(blended_image, f"{dst} mm", [30, 30], cv2.FONT_HERSHEY_SIMPLEX, 1.2, WHITE_COLOR, 2)
        return blended_image

