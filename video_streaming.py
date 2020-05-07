import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    print(frame)
    print(type(frame))

    w,h,d = frame.shape
    w,h,d = int(w), int(h), int(d)
    # print(type(w), type(h), type(d))

    # draw rectangle
    cv2.rectangle(frame,(int(w/2),int(w/2)),(int(h/2),int(h/2)),(0,255,0),7)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    
    # press q to stop video 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()