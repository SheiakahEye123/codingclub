import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("this.png")
cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

def findMapEdges(img):
    grayimg = img[:,:,2]
    thresh = cv2.adaptiveThreshold(grayimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    blank = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(thresh, contours, 30, (0,0,255), 300)
    return thresh

cv2.imshow("Map shit",findMapEdges(img))
cv2.waitKey(0)