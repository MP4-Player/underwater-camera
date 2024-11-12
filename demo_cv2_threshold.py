#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np


threshold = 100
current_depth = 0


def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value

def raw_depth_to_meters(threshhold):
    if threshold < 2047:
        return 1.0 / (threshold * -0.0030711016 + 3.3309495161)
    else:
        return 0

def show_depth():
    global threshold
    global current_depth

    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    cv2.putText(depth, f"{raw_depth_to_meters(threshold)} mm", [30, 30], cv2.FONT_HERSHEY_SIMPLEX, 1.2, [255, 255, 255], 2)

    cv2.imshow('Depth', depth)


def show_video():
    cv2.imshow('Video', frame_convert2.video_cv(freenect.sync_get_video()[0]))


cv2.namedWindow('Depth')
cv2.namedWindow('Video')
cv2.createTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv2.createTrackbar('depth',     'Depth', current_depth, 2048, change_depth)

print('Press ESC in window to stop')


while 1:
    show_depth()
    show_video()
    if cv2.waitKey(10) == 27:
        break
