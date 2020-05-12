import numpy as np
import cv2
from alphabet_dictionary.hand_convex_hull import *
from alphabet_dictionary.hand import *
from app import *


cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

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

    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    # mask = cv2.inRange(crop_img, lower, upper)

    converted = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(crop_img, crop_img, mask = skinMask)

    # print(skin)

    user_hand = Hand(image = skin)
    cv2.putText(frame, 'Sign letter in the box', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    # cv2.imshow("cropped", crop_img)
    cv2.imshow("skin", skin)
    
    # press q to stop video 
    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        cv2.imwrite('user_image.png',skin)
        cv2.destroyAllWindows()
        break

im = cv2.imread("user_image.png")
im = cv2.GaussianBlur(im, (5, 5), 0)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
(thr, bw) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # Black is foreground, white is background
hand, hierarchy = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
area = cv2.contourArea(hand[0])

if area > 1000:  # Check to make sure we've got a good picture!!
    letter = aslToEnglish("user_image.png")
    print("The letter you signed is " + letter)
else:
    print("Take another picture!!")

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

