import cv2

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


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            break
        
        cv2.imshow('Canny_video', process_frame(frame))


        if cv2.waitKey(1) == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()