#!/usr/bin/env python
from gui import *
from kinect import depth2PointCloud
import freenect
import frame_convert2

def process_images():
    """
    В этой функции надо получать в цикле изображение цвета RGB в виде ndarray из numpy и матрицу с координатами.
    Матрица имеет размерности AxB, где А - ширина изображения, B - высота изображения. Каждая ячейка матрицы содержит
    список координат XYZ. Обычно камеры глубины дают облако точек XYZ в виде одномерного массива, где каждый элемент
    это список координат XYZ. Это нам не подходит, но можно сделать reshape этого вектора по размеру изображения.
    Либо камера глубины дает нам картинку глубины, где в каждом пикселе хранится расстояние до пикселя. Это тоже нам не
    подходит, в этом случае с помощью матрицы калибровки нужно сделать пересчет расстояний до координат XYZ и записать в
    те же ячейки матрицы.
    Далее нужно подать эти переменные в функцию расчета расстояний и функцию отображения, calc_dist и show
    соответственно.

    Камера реалсенс дает картинку глубины и я ее с помощью функции depth2PointCloud преобразовываю в матрицу с
    координатами
    Камера OAK D дает и картинку глубины, и облако точек, но облако точек проще преобразовать в матрицу точек, чем
    картинку глубины, просто с помощью функции reshape. В файле oakd внизу есть

    Все координаты указывать в миллиметрах, там видно, что я значения делю на 1000, но это не так важно, если что, от
    этого не перестанет работать расчет, просто будет не отмасштабировать
    :return:
    """
    window = CvWindow()

    # Все что связанно с реалсенсом закомментировано, нужно получить с твоей камеры две матрицы и подставить в функции
    # Realsensed415Cam = DepthCamera(resolution_width, resolution_height)
    # depth_scale = Realsensed415Cam.get_depth_scale()

    while True:

        # ret, depth_raw_frame, color_raw_frame = Realsensed415Cam.get_raw_frame()
        # if not ret:
        #     print("Unable to get a frame")

        rgb_image = freenect.sync_get_video()[0]
        # print("---------", rgb_image.shape, rgb_image[0])
       
        depth = freenect.sync_get_depth()[0]

        raw_depth_mat = depth
        print(raw_depth_mat[0][2])
        for pix in raw_depth_mat:
            pix[0] = raw_depth_to_meters(pix[0]) * 10
            pix[1] = raw_depth_to_meters(pix[1]) * 10
            pix[2] = raw_depth_to_meters(pix[2]) * 10
        print(raw_depth_mat[0][2])

        rows = [depth[i, :] for i in range(depth.shape[0])]
        cols = [depth[:, i] for i in range(depth.shape[1])]
        depthpoints = depth2PointCloud(depth)
        # depthpoints = depth2xyzuv(depth)
        # points_xyz = depth2PointCloud(depthpoints, 1)
        # print("---------", depthpoints.shape, depthpoints[0])
        
        dst = calc_dist(depthpoints, window.measurePoints)
        window.show(rgb_image, dst)

def raw_depth_to_meters(raw_depth):
    if raw_depth < 2047:
        return 1.0 / (raw_depth * -0.0030711016 + 3.3309495161)
    else:
        return 0

def depth2xyzuv(depth, u=None, v=None):
    if u is None or v is None:
        u,v = np.mgrid[:480,:640]  
    # Build a 3xN matrix of the d,u,v data
    C = np.vstack((u.flatten(), v.flatten(), depth.flatten(), 0*u.flatten()+1))
    # Project the duv matrix into xyz using xyz_matrix()
    X,Y,Z,W = np.dot(xyz_matrix(),C)
    X,Y,Z = X/W, Y/W, Z/W
    xyz = np.vstack((X,Y,Z)).transpose()
    xyz = xyz[Z<0,:]
    # Project the duv matrix into U,V rgb coordinates using rgb_matrix() and xyz_matrix()
    return xyz

def xyz_matrix():
  fx = 5.942143
  fy = 5.910405
  a = -0.0030711
  b = 3.3309495
  cx = 3.39307
  cy = 2.42739
  mat = np.array([[1/fx, 0, 0, -cx/fx],
                  [0, -1/fy, 0, cy/fy],
                  [0,   0, 0,    -1],
                  [0,   0, a,     b]])
  return mat

if __name__ == '__main__':
    process_images()
