import math
from collections import Counter


BLACK_COLOR = [0, 0, 0]
WHITE_COLOR = [255, 255, 255]
BLUE_COLOR = [0, 0, 255]
RED_COLOR = [255, 0, 0]
GREEN_COLOR = [0, 255, 0]


medianDist = 0
medianDistArray = []


def most_unique_elements(list_):
    lists = [list_, [0]]
    freq_list = [Counter(lst) for lst in lists]
    max_freq = max(freq_list, key=len)
    return list(max_freq.keys())


def calc_dist(points_xyz_mat, points):
    if len(points) == 2:
        x1 = points_xyz_mat[points[0][1], points[0][0]][0]
        y1 = points_xyz_mat[points[0][1], points[0][0]][1]
        z1 = points_xyz_mat[points[0][1], points[0][0]][2]
        x2 = points_xyz_mat[points[1][1], points[1][0]][0]
        y2 = points_xyz_mat[points[1][1], points[1][0]][1]
        z2 = points_xyz_mat[points[1][1], points[1][0]][2]

        print("Z1:", z1 * 100)
        print("Z2:", z2 * 100)

        dst = round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) * 1000)
        return calc_median(dst)
    else:
        return 0


def calc_median(dst):
    global medianDistArray, medianDist
    medianDistArray.append(dst)
    if len(medianDistArray) > 25:
        medianDist = most_unique_elements(medianDistArray)[0]
        medianDistArray.clear()
    return medianDist

