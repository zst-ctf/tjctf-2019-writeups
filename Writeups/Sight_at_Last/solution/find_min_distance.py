import cv2
import numpy as np
from scipy.spatial import distance

def main(filename='test.png', debug=False):
    # Read the input image
    im = cv2.imread(filename)
    # Convert to grayscale
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Threshold the image
    ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the image
    # https://stackoverflow.com/questions/25504964/opencv-python-valueerror-too-many-values-to-unpack
    _, ctrs, hier = cv2.findContours(
        im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # To hold centers of circles
    circle_points = []

    # Get rectangles bounding each ciecle
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]
    for rect in rects:
        # get parameters
        originX = rect[0]
        originY = rect[1]
        width = rect[2]
        height = rect[3]

        # calculate center
        centerX = originX + width // 2
        centerY = originY + height // 2

        # Draw debugging rectangles & center point
        if debug:
            cv2.rectangle(im, (originX, originY),
                (originX + width, originY + height), (0, 0, 255),
                thickness=2)
            cv2.circle(im, (centerX, centerY),
                radius=2, color=(0, 0, 255), thickness=-1)

        # append to list of circles
        circle_points.append((centerX, centerY))

    # Calculate distance between each pairs
    print('Found {} circles'.format(len(circle_points)))
    s1 = circle_points
    s2 = circle_points
    distances = distance.cdist(s1, s2)

    # Remove points between itself
    # https://stackoverflow.com/a/53541263
    distances = distances.flatten()
    distances = distances[distances != 0]
    if debug:
        print(distances)

    # Find min distance
    min_dist = distances.min()
    if debug:
        print('Min distance:', min_dist)

    if debug:
        cv2.imshow("Resulting Image with Rectangular ROIs", im)
        cv2.waitKey()

    return min_dist

if __name__ == '__main__':
    main(debug=True)
