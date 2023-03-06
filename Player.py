import pygame

pygame.init()
class YourPlayer():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.minix = 0
        self.miniy = 0
        self.weapons = []
        self.a = [False,False,False,False,False,False]
        self.velx = 0
        self.vely = 0
        self.ETM = 0
        self.swordimg = pygame.transform.scale(pygame.image.load("sword.png"), (64, 64))
        self.parrydegcounter = 0

    def accelerate(self, speed):
        accx = 0
        accy = 0
        if self.a[0] == True:
            # w
            accy = -1
        if self.a[1] == True:
            # a
            accx = -1
        if self.a[2] == True:
            # s
            accy = 1
        if self.a[3] == True:
            # d
            accx = 1

        self.velx += accx * speed * self.ETM
        self.vely += accy * speed * self.ETM

        self.vely *= 0.9
        self.velx *= 0.9

        return

    def blockParryDodge(self, screen):
        swordcopy = self.swordimg.copy()
        if self.a[4] and self.parrydegcounter <= 0:
            self.parrydegcounter = 360
            return
        androtatecopy = pygame.transform.rotate(swordcopy,10)
        self.parrydegcounter-=1
        screen.blit(androtatecopy, (960, 540))

