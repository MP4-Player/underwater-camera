import numpy as np


def depth2PointCloud(depth):
    """
    Функция преобразует изображение глубины в облако точек

    depth - изображение глубины, просто матрица ndarray в формате float32, каждый пиксель матрицы изображения содержит
    расстояние до объекта в этом пикселе

    параметры ppx, ppy, fx, fy - параметры калибровочной матрицы, взяты с реалсенс, нужно калибровать конкретную камеру,
    эти для другой вряд ли подойдут

    :param depth:
    :return:
    """
    depth_scale = 0.001  # Если значения в матрице depth в метрах, то коэффициент 0.001, чтобы преобразовать в мм
    ppx = 313.7337646484375
    ppy = 236.78021240234375
    fx = 619.4382934570312
    fy = 618.6329956054688
    depth = depth * depth_scale
    rows, cols = depth.shape

    c, r = np.meshgrid(np.arange(cols), np.arange(rows), sparse=True)
    r = r.astype(float)
    c = c.astype(float)

    z = depth
    x = z * (c - ppx) / fx
    y = z * (r - ppy) / fy

    pointsxyz = np.dstack((x, y, z))

    return pointsxyz