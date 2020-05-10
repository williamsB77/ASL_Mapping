import numpy as np
import cv2

class Hand:
    def __init__(self, file_name):

        self.file_name = file_name
        self.convex_hull_area = 0

        im_name = self.file_name
        im = cv2.imread(im_name)

        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        self.contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        self.all_counter_hull_areas = {}

        for i in range(1,len(self.contours)): 
            counter_hull = cv2.convexHull(self.contours[i])
            counter_hull_area = cv2.contourArea(counter_hull)
            self.all_counter_hull_areas[counter_hull_area] = i

        biggest_hull_area = (max(self.all_counter_hull_areas.keys()))
        hand_counter_index = self.all_counter_hull_areas[biggest_hull_area]

        self.hand_counter = self.contours[hand_counter_index]
        self.hand_convex_hull = cv2.convexHull(self.hand_counter)
        self.hand_convex_hull_area = cv2.contourArea(self.hand_convex_hull)

        # cv2.drawContours(im, [self.hand_counter], 0, (0,0,255), 3)


    def show_hand_counter(self):
        im_name = self.file_name
        im = cv2.imread(im_name)

        # hand_counter = contours[hand_counter_index]

        cv2.drawContours(im, [self.hand_counter], 0, (0,0,255), 3)

        cv2.imshow('frame',im)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


import glob
all_hand_pics = [f for f in glob.glob("*.PNG")] # based off of alphabet_dictionary folder - make sure that you are pointing to it

for hand in all_hand_pics:
    im_name = hand
    letter = Hand(im_name)
    letter.show_hand_counter()