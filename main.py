import numpy as np
import cv2
import pygame
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(5000)
oimg = cv2.imread("this.png")
pygame.display.init()
screen = pygame.display.set_mode(size=(1920, 1080), vsync=240)

playerpos = (0,0)
playerposT = (int(playerpos[0]/64),int(playerpos[1]/64))

class tile:
    def __init__(self, filecall, discovered, x, y):
        self.filecall = filecall
        self.discovered = discovered
        self.x = x
        self.y = y

    def draw(self):
        if playerpos[0] - 20 <= self.x <= playerpos[0] + 20 and playerpos[1] - 20 <= self.y <= playerpos[1] + 20:
            tileimg = pygame.transform.scale(pygame.image.load(self.filecall), (64,64))
            screen.blit(tileimg, (self.x * 64 + playerpos[0], self.y * 64 + playerpos[1]))


class cvImageProccesing:
    def __init__(self, img):
        self.img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        self.map = None

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
                break
        return blank

    def findMap(self, blank):
        self.map = []
        imgmap = cv2.resize(blank, (80, 106), interpolation=cv2.INTER_AREA) * 255
        xs, ys = imgmap.shape
        for i in range(xs):
            mini = []
            for e in range(ys):
                mini.append(tile(filecall="sea.png", discovered=False, x=i, y=e))
            self.map.append(mini)
        self.forFindMap(imgmap, self.map, int(len(self.map[0])/2), int(len(self.map)/2))

    def forFindMap(self, imgmap, map, x, y):
        checklist = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        for i in checklist:
            if 0 <= i[0] < len(map) and 0 <= i[1] < len(map[0]):
                if imgmap[i[0]][i[1]] != 0:
                    continue
                map[i[0]][i[1]] = tile(filecall="grass.png", discovered=True, x=i[0], y=i[1])
                imgmap[i[0]][i[1]] = 100
                self.forFindMap(imgmap, map, i[0], i[1])

        plt.figure(0)
        plt.imshow(imgmap)
        plt.show()
        return


imageproccesing = cvImageProccesing(oimg)
imageproccesing.findMap(imageproccesing.createMap())


def main():
    while True:
        for t in imageproccesing.map:
            for te in t:
                te.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
