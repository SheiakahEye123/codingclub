import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pygame
import sys

oimg = cv2.imread("this.png")
phase = "1"
pygame.display.init()
screen = pygame.display.set_mode(size=(1920, 1080), vsync=240)


class tile:
    def __init__(self, filecall, discovered, x, y):
        self.filecall = (filecall + phase)
        self.discovered = discovered
        self.x = x
        self.y = y

    def draw(self):
        tileimg = pygame.image.load(self.filecall)
        screen.blit(tileimg, self.x, self.y)


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
        blank = np.zeros_like(self.img[:, :, 2])
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
        for i in range(xs):
            mini = []
            for e in range(ys):
                mini.append(tile(filecall="sea",discovered=False, x=i,y=e))
            map.append(mini)
        imgmap = cv2.resize(blank, (80, 106), interpolation=cv2.INTER_AREA) * 255

        for x in range(len(imgmap)):
            for y in range(len(imgmap[0])):
                self.forFindMap(imgmap, map, x, y)

        plt.figure(2)
        plt.imshow(imgmap)
        plt.pause(0.01)

    def forFindMap(self, imgmap, map, x, y):
        checklist = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1], [x - 1, y], [x, y], [x + 1, y], [x - 1, y + 1],
                     [x, y + 1], [x + 1, y + 1]]
        for i in checklist:
            if 0 <= i[0] < len(imgmap[0]) and 0 <= i[1] < len(imgmap):
                if i[0] != x and i[1] != y and map[i[0]][i[1]] is None:
                    if imgmap[i[0]][i[1]] == 0:
                        map[i[0]][i[1]] = tile(filecall="grass", discovered=True, x=i[0], y=i[1])
                        imgmap[i[0]][i[1]] = 100

        plt.figure(2)
        plt.imshow(imgmap)
        plt.pause(0.01)

        return


imageproccesing = cvImageProccesing(oimg)
imageproccesing.findMap(imageproccesing.createMap())
plt.show()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
