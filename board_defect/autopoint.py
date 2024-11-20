import cv2
import numpy as np


def process_image(image_path):
    
    img = cv2.imread(image_path)
    img = cv2.medianBlur(img, 3)


    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    t_lower = 70 
    t_upper = 125 
    aperture_size = 3 

    
    canny_frame = cv2.Canny(gray_frame, t_lower, t_upper, apertureSize=aperture_size)

  
    contours, hierarchy = cv2.findContours(canny_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
   
    cv2.drawContours(img, contours, -1, (255, 0, 255), 1)

    return img, contours

def mouse_callback(x, y, flags, param, contours):
    
    min_distance = float('inf')
    contur_point = None

    for contour in contours:
        for point in contour: 
            
            distance = np.linalg.norm(np.array((x, y)) - point[0])
            
            if distance < min_distance and distance <= 10:
                min_distance = distance
                contur_point = point[0]

    if contur_point is not None:
        return contur_point[0], contur_point[1]
    else:
        return x, y

def main():
    global img, contours, points

    image_path = 'test4.jpg'

    img, contours = process_image(image_path)

    points = []

    
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_callback)


    while True:

        cv2.imshow('Image', img)

        for point in points:

            cv2.circle(img, point, 2, (0, 255, 0), -1)


        if cv2.waitKey(1) == ord('q'):
            break


    cv2.destroyAllWindows()
    print("Список точек:",points)


if __name__ == "__main__":
    main()
