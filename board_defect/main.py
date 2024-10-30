import cv2

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break


    frame = cv2.medianBlur(frame, 3)


    gray_frame = cv2.cvtColor(frame, cv2.RETR_TREE)


    t_lower = 70  # Lower Threshold 
    t_upper = 125  # Upper threshold 
    aperture_size = 3  # Aperture size 
    #L2Gradient = True  # Boolean 


    canny_frame = cv2.Canny(gray_frame, t_lower, t_upper, 
                     apertureSize=aperture_size)
    


    cv2.imshow('Canny_video', canny_frame)


    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()