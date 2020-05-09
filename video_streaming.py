import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # print(frame)
    # print(type(frame))
    
    w,h,d = frame.shape
    w,h,d = int(w), int(h), int(d)
    # print(type(w), type(h), type(d))

    radius = 15
    thickness = 7

    # draw rectangle -- #TODO make rectangle bigger
    start_point = (int(h/2),int(w/2))
    end_point = (0,w)
    cv2.rectangle(frame,start_point,end_point,(0,255,0),7)

    cropped_w, cropped_h = int(w/2), int(h/2)

    crop_img = frame[cropped_w:, : cropped_h]
    
    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow("cropped", crop_img)
    
    # press q to stop video 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()