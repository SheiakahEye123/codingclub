import math

import numpy as np
import cv2
import pygame
import sys
import matplotlib.pyplot as plt
import Player
import time
import Opp
import random

oimg = cv2.imread("this.png")
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode(size=(1920, 1080), vsync=240)
sys.setrecursionlimit(5000)

player = Player.YourPlayer()


class tile:
    def __init__(self, filecall, discovered, x, y):
        self.filecall = filecall
        self.tileimg = pygame.transform.scale(pygame.image.load(self.filecall), (64, 64))
        self.discovered = discovered
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(self.tileimg, ((self.x - player.x) * 64 + 960, (self.y - player.y) * 64 + 540))
        return


class cvImageProccesing:
    def __init__(self, img):
        self.img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        self.map = []

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
        imgmap = cv2.resize(blank, (80, 106), interpolation=cv2.INTER_AREA) * 255
        xs, ys = imgmap.shape
        for i in range(xs):
            mini = []
            for e in range(ys):
                mini.append(tile("sea.png", False, i, e))
            self.map.append(mini)
        self.forFindMap(imgmap, self.map, int(len(self.map[0]) / 2), int(len(self.map) / 2))
        return

    def forFindMap(self, imgmap, map, x, y):
        self.map[y][x].tileimg = pygame.transform.scale(pygame.image.load("grass.png"), (64, 64))
        self.map[y][x].discovered = True
        if imgmap[y - 1][x] == 0:
            imgmap[y][x] = 100
            self.forFindMap(imgmap, map, x, y - 1)
        if imgmap[y + 1][x] == 0:
            imgmap[y][x] = 100
            self.forFindMap(imgmap, map, x, y + 1)
        if imgmap[y][x - 1] == 0:
            imgmap[y][x] = 100
            self.forFindMap(imgmap, map, x - 1, y)
        if imgmap[y][x + 1] == 0:
            imgmap[y][x] = 100
            self.forFindMap(imgmap, map, x + 1, y)
        return


imageproccesing = cvImageProccesing(oimg)
imageproccesing.findMap(imageproccesing.createMap())

newopp = Opp.Opp(40, 30, player)


def main():
    global atcoolopp
    et = 0
    speed = 0.5
    while True:
        st = time.time()
        screen.fill((0, 0, 0))
        for t in imageproccesing.map:
            for te in t:
                if player.x - 20 < te.x < player.x + 20 and player.y - 20 < te.y < player.y + 20:
                    te.draw()

        temp = pygame.mouse.get_pos()
        player.mousepos = (temp[0] - 960, temp[1] - 540)
        player.accelerate(speed, screen)
        newopp.player = player
        newopp.accelerate(speed / 2)
        if player.x <= 0:
            player.x = 0.1
        elif player.x >= len(imageproccesing.map[0]):
            player.x = len(imageproccesing.map[0]) - 1
        elif 0 < player.x < 80:
            player.x += player.velx

        if player.y <= 0:
            player.y = 0.1
        elif player.y >= len(imageproccesing.map):
            player.y = len(imageproccesing.map) - 1
        elif 0 < player.y < 106:
            player.y += player.vely


        player.blockParryDodge(screen)

        pygame.draw.rect(screen, (255, 0, 0), (960, 540, 10, 10))

        newopp.x += newopp.velx
        newopp.y += newopp.vely

        font = pygame.font.Font('freesansbold.ttf', 32)

        for event in pygame.event.get():
            player.mousebutton = pygame.mouse.get_pressed(3)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.a[0] = True
                if event.key == pygame.K_a:
                    player.a[1] = True
                if event.key == pygame.K_s:
                    player.a[2] = True
                if event.key == pygame.K_d:
                    player.a[3] = True
                if event.key == pygame.K_f:
                    player.a[4] = True
                if event.key == pygame.K_q:
                    player.a[5] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.a[0] = False
                if event.key == pygame.K_a:
                    player.a[1] = False
                if event.key == pygame.K_s:
                    player.a[2] = False
                if event.key == pygame.K_d:
                    player.a[3] = False
                if event.key == pygame.K_f:
                    player.a[4] = False
                if event.key == pygame.K_q:
                    player.a[5] = False

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        player.draw(screen)
        newopp.draw(screen)

        if player.health > 0:
            pygame.draw.rect(screen, (255,25,25), (960-player.health,500,100-player.health,10))

        rect = pygame.Rect(860,540,100,100)

        if rect.colliderect((((newopp.x-player.x) * 64 + 960),((newopp.y-player.y) * 64 + 540),64,64)):
            newopp.health -= 1
            if player.blocking:
                if player.pc < 2:
                    cra = pygame.mixer.Sound("stun.mp3")
                    pygame.mixer.Sound.play(cra)
                    pygame.mixer.music.stop()
                    newopp.stun = 4
            else:
                player.health -= 5
                player.vely -= 0.25

            if player.blocking and newopp.y <= player.y:
                pygame.draw.rect(screen, (255, 255, 0), (960, 540, 50, 50))
                newopp.vely += -0.25
            else:
                player.health -= 5


        if player.atcbox.colliderect((((newopp.x-player.x) * 64 + 960),((newopp.y-player.y) * 64 + 540),64,64)):
            newopp.health -= player.dmg
            newopp.velx -= 0.25

            if random.randint(0,11) == 1:
                cra = pygame.mixer.Sound("stun.mp3")
                pygame.mixer.Sound.play(cra)
                pygame.mixer.music.stop()
                player.vely -= 0.5
                player.pc = 10




        pygame.display.update((0, 0), (1920, 1080))
        player.ETM = abs(st - et)
        newopp.ETM = abs(st - et)
        et = st


if __name__ == "__main__":
    main()
