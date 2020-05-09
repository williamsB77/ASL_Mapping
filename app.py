"""
Classifier of American Sign Language hand movements for translation
"""


import cv2
import numpy


# Method to parse the images
def true_dictionary(images_file):
    # Open file somewhere to read to t_im
    true_images = images_file

    targets = {}
    al_count = 0
    for x in true_images:
        objects = []
        al = cv2.imread(x, 1)
        hand = cv2.findContours(al, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        init_area = cv2.contourArea(hand)

        objects.append(init_area)  # Add to initial differentiation list to narrow down choices
        objects.append(hand)

        targets[al_count] = objects
        al_count += 1

    return targets


def aslToEnglish(image):
    letter = 0
    # First, make a dictioray with the true images
    targets = true_dictionary(alphabet_dictionary)

    # Reads and processes the image
    im = cv2.imread(image, 1)
    im = cv2.GaussianBlur(im, (5, 5), 0)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    (thr, bw) = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)  # Black is foreground, white is background

    # Create a bounding box around the image
    hand = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # (bX, bY, bW, bH) = cv2.boundingRect(hand)
    area = cv2.contourArea(hand)
    similar = []

    for possible in targets:
        l = targets[possible]
        a = l[0]
        diff = abs(area - a)

        if diff <= 10:
            similar.append(possible)

    return letter


if __name__ == '__main__':
    print("Input your letter:")
    image = input()
    eng = aslToEnglish(image)
    print("The letter you're looking for is: " + eng)
