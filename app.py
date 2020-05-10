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


def shapeCoordinate(path1, path2, value):

    theSum = 0
    diff = 0
    boundary = 2 ** value
    path2 = path2 + ".PNG"

    image1 = cv2.imread(path1, 1)
    image1 = cv2.GaussianBlur(image1, (5, 5), 0)
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    (thr, bw1) = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)

    im_bin = {}
    for val in range(2):
        im_bin[val] = 0
        # Check each pixel for value
        for j in range(126):
            for k in range(273):
                red, green, blue = bw1[k][j]
                p = (red + green + blue) / 3  # Intensity value
                if p <= boundary:
                    im_bin[0] += 1
                else:
                    im_bin[1] += 1

    image2 = cv2.imread(path2, -1)
    image2 = cv2.GaussianBlur(image2, (3, 3), 0)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    (thr2, bw2) = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)

    y_bin = {}
    for val2 in range(2):
        y_bin[val2] = 0
        # Gotta get the pixel values of these too
        for j in range(126):
            for k in range(273):
                red, green, blue = bw2[k][j]
                p = (red + green + blue) / 3  # Intensity value
                if p <= boundary:
                    im_bin[0] += 1
                else:
                    im_bin[1] += 1

    denom = 127 * 273
    for bin in range(2):
        ibin = im_bin
        ybin = y_bin[bin]
        num = abs(ibin - ybin)
        diff = num / denom
        theSum += diff

    return theSum


def aslToEnglish(image):
    letter = 0
    # First, make a dictionary with the true images [letter, convex area]
    targets = true_dictionary()
    #print(targets)

    # Reads and processes the image
    im = cv2.imread(image, 1)
    width = 126
    height = 273
    dim = (width, height)
    resize = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)

    im = cv2.GaussianBlur(resize, (5, 5), 0)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    (thr, bw) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # Black is foreground, white is background

    hand, hierarchy = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = cv2.convexHull(hand[0])
    area = cv2.contourArea(hull)
    #area = area * 4

    # Narrow down the list until we get to 1 by area/orientation/solidity
    similar = []
    for possible in targets:
        l = targets[possible]
        a = l[1]
        diff = abs(area - a)

        if diff <= 5000:
            print(l[0])
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
        #print(aspect)
        if aspect < .71:
            key = 0
        else:
            key = 1

        #print(similar)
        for possible in similar:
            l = targets[possible]
            x2, y2, w2, h2 = cv2.boundingRect(l[2])
            rat = w2 / h2
            if key == 0:
                if rat > .71:
                    similar.remove(possible)
            if key == 1:
                if rat < .71:
                    similar.remove(possible)
        #print(similar)


    if len(similar) == 1:
        l = targets[similar[0]][0]
        path = l[0].split('/')
        letter = path[1]
    else:
        # Check solidity -- how well the area covers its convex hull shape
        rArea = cv2.contourArea(hand[0])
        solidity = rArea / area
        print(solidity)

        for possible in similar:
            l = targets[possible]
            print(l[0])
            hArea = l[1]
            area = cv2.contourArea(l[2])
            s = area / hArea
            print(s)

    return letter

"""
testing purposes
if __name__ == '__main__':

    eng = aslToEnglish("IMG_0639.JPG")
    print(eng)
    #print("Input your letter:")
    #image = input()
    #eng = aslToEnglish(image)

    #listing1 = true_dictionary(alphabet_dictionary)
    #print("The letter you're looking for is: " + eng)
"""