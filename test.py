#!/usr/bin/python
import freenect
import cv2
def get_video():
    array,_ = freenect.sync_get_video(0,freenect.VIDEO_IR_10BIT)
    return array
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        frame = get_video()
        #display IR image
        cv2.imshow('IR image',frame)
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
