#!/usr/bin/env python
import freenect
import cv2
import frame_convert2

cv2.namedWindow('Depth')
cv2.namedWindow('Video')
print('Press ESC in window to stop')

def process_frame(frame):
    frame = cv2.medianBlur(frame, 3)


    gray_frame = cv2.cvtColor(frame, cv2.RETR_TREE)


    t_lower = 70 
    t_upper = 125 
    aperture_size = 3 

    canny_frame = cv2.Canny(gray_frame, t_lower, t_upper, apertureSize=aperture_size)

    contours, hierarchy = cv2.findContours(canny_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)

    return frame

def get_depth():
    print("---------", frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0]).ndim)
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])


while 1:
    cv2.imshow('Depth', process_frame(get_depth()))
    cv2.imshow('Video', process_frame(get_video()))
    if cv2.waitKey(10) == 27:
        break
