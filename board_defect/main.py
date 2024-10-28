import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    if not ret:
        break

    canny_frame = cv2.Canny(frame, 100, 100)

    cv2.imshow('Canny_video', canny_frame)
    if cv2.waitKey(1) == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()