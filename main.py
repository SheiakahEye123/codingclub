import numpy as np
import cv2
import matplotlib.pyplot as plt
oimg = cv2.imread("this.png")
class cvImageProccesing:
    def __init__(self, img):
        self.img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    def createMap(self):
        grayimg = self.img[:, :, 2]
        thresh = ~cv2.adaptiveThreshold(grayimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 2)
        kernel = np.ones((3, 3), np.uint8)
        gaussianimg = cv2.GaussianBlur(cv2.erode(thresh, kernel, iterations=1), (5, 5), 0, 0)
        dilateimg = cv2.dilate(gaussianimg, kernel, iterations=1)
        contours, hier = cv2.findContours(dilateimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        xs, ys, _ = self.img.shape
        blank = np.zeros_like(self.img[:,:,2])
        for c in range(len(contours)):
            if cv2.contourArea(contours[c]) > (xs * ys) / 30:
                cv2.drawContours(blank, contours, c, 255, 1)
                bigc = c
                break
        plt.figure(1)
        plt.imshow(blank)
        plt.pause(0.01)
        return blank
    def findMap(self, blank):
        xs, ys = blank.shape
        map = [[]]
        imgmap = cv2.resize(blank, (80,106), interpolation = cv2.INTER_AREA) * 255



        plt.figure(2)
        plt.imshow(imgmap)
        plt.pause(0.01)

    def forFindMap(imgmap, map, x, y):
        if imgmap[x][y] == 255:
            return
        if map[x][y] ==


imageproccesing = cvImageProccesing(oimg)
imageproccesing.findMap(imageproccesing.createMap())

plt.show()
