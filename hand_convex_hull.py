import numpy as np
import cv2

def get_convex_hull(im_filename):
    im = cv2.imread(im_name)

    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(im, contours, -1, (0,255,0), 3)

    cnt = contours[1]
    cv2.drawContours(im, [cnt], 0, (0,255,0), 3)

    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)

    return(hull_area)

    # to see the image with the counters 
    # cv2.imshow('frame',im)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# im_name = 'a.PNG' 
# print(get_convex_hull(im_name))