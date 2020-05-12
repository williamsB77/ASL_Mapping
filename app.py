"""
Parse the input to letters
"""

import cv2
import glob
import numpy


# Method to parse the images
def true_dictionary():
    targets = {}
    al_count = 0
    folder = glob.glob("alphabet/*.PNG")

    for img in folder:
        al = cv2.imread(img)

        objects = []
        l = img.split('.')
        letter = l[0]
        objects.append(letter)

        im_bw = cv2.cvtColor(al, cv2.COLOR_BGR2GRAY)
        (thr, bw) = cv2.threshold(im_bw, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hand = contours[0]
        hull = cv2.convexHull(hand)
        init_area = cv2.contourArea(hull)

        objects.append(init_area)
        objects.append(hand)

        targets[al_count] = objects
        al_count += 1

    return targets


def aslToEnglish(image):
    letter = 0
    # First, make a dictionary with the true images [letter, convex area]
    targets = true_dictionary()
    #print(targets)

    # Reads and processes the image
    im = cv2.imread(image, 1)
    im = cv2.GaussianBlur(im, (5, 5), 0)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    (thr, bw) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # Black is foreground, white is background

    hand, hierarchy = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = cv2.convexHull(hand[0])
    area = cv2.contourArea(hull)
    area = area * 500
    print(area)

    # Narrow down the list until we get to 1 by area/orientation/solidity
    similar = []
    for possible in targets:
        l = targets[possible]
        a = l[1]
        diff = abs(area - a)

        if diff <= 3000:
            #print(l[0])
            similar.append(possible)

    #After we have all the letters with similar area make up, find similar shape
    if len(similar) == 1:
        l = targets[similar[0]][0]
        path = l[0].split('/')
        letter = path[1]

    else:
        # Check orientation
        x1, y1, w, h = cv2.boundingRect(hand[0])
        aspect = w / h
        print(aspect)
        if aspect < .71:
            key = 0
        else:
            key = 1

        print(similar)
        for possible in similar:
            l = targets[possible]
            x2, y2, w2, h2 = cv2.boundingRect(l[2])
            #print(l[0])
            rat = w2 / h2
            #print(rat)
            if key == 0:
                if rat > .71:
                    similar.remove(possible)
            if key == 1:
                if rat < .71:
                    similar.remove(possible)
        print(similar)


    if len(similar) == 1:
        l = targets[similar[0]][0]
        path = l[0].split('/')
        letter = path[1]
    else:
        # Check solidity -- how well the area covers its convex hull shape
        rArea = cv2.contourArea(hand[0])
        rArea = rArea * 100
        solidity = rArea / area
        print(solidity)

        closest = 1
        num = 26
        for possible in similar:
            l = targets[possible]
            print(l[0])
            cArea = cv2.contourArea(l[2])
            s = rArea / cArea  # Check this out!!
            print(s)
            d = abs(solidity - s)
            if d < closest:
                closest = d
                num = possible

        if num is not 26:
            final = targets[num]
            theImage = final[0]
            i = theImage.split('/')
            letter = i[1]
        else:
            letter = "I'm sorry, we cannot recognize the image"

    return letter


# Testing purposes
#if __name__ == '__main__':

    #eng = aslToEnglish("user_image.PNG")
    #print(eng)
    #print("Input your letter:")
    #image = input()
    #eng = aslToEnglish(image)

    #listing1 = true_dictionary()
    #print(listing1)
    #print("The letter you're looking for is: " + eng)