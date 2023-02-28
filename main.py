import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("this.png")
cv2.cvtColor(img, cv2.COLOR_RGB2HSV)


def findMapEdges(img):
    grayimg = img[:, :, 2]
    # gets grayscale img
    thresh = ~cv2.adaptiveThreshold(grayimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 2)
    # adaptivethreshold finds "edges"
    kernel = np.ones((3, 3), np.uint8)
    erodeimg = cv2.erode(thresh, kernel, iterations=1)
    gaussianimg = cv2.GaussianBlur(erodeimg, (5, 5), 0, 0)
    dilateimg = cv2.dilate(gaussianimg, kernel, iterations=1)
    # contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(gaussianimg, contours, 30, (0,0,255), 30)
    return dilateimg

def findcs(img):
    contours, hier = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y = img.shape
    for c in range(len(contours)):
        if cv2.contourArea(contours[c]) > 40000:
            (x, y), radius = cv2.minEnclosingCircle(contours[c])
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(img,center,radius, 255,2)
            cv2.drawContours(img, contours, c, 255, 1)
            bigc = c
            break

    plt.figure(1)
    plt.imshow(img)
    plt.pause(0.01)

    return bigc

thing = findcs(findMapEdges(img))

plt.show()
