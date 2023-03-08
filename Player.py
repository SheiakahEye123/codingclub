import math

import pygame
import Util

pygame.init()
pygame.mixer.init()
util = Util.Util()


class YourPlayer():
    def __init__(self):
        self.x = 40
        self.y = 50
        self.a = [False, False, False, False, False, False, False]
        self.velx = 0
        self.vely = 0
        self.ETM = 0
        self.swordimg = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("sword.png"), (64, 64)), 45)
        self.swordbox = self.swordimg.get_rect()
        self.pc = 0
        self.rollcooldown = 0
        self.mousebuttons = (False,False,False)
        self.mousepos = ()
        self.img = pygame.transform.scale(pygame.image.load("knight.png"), (64,64))
        self.stun = False
        self.atcbox = self.swordimg.get_rect()
        self.health = 100
        self.dmg = 5
        self.blocking = False

    def accelerate(self, speed, screen):
        accx = 0
        accy = 0
        if self.a[0] == True:
            # w
            accy += -1
        if self.a[1] == True:
            # a
            accx += -1
        if self.a[2] == True:
            # s
            accy += 1
        if self.a[3] == True:
            # d
            accx += 1
        if self.a[5] and self.rollcooldown <= 0:
            d = math.hypot(self.mousepos[0], self.mousepos[1]) * 5
            self.velx += (self.mousepos[0] / d) * 3
            self.vely += (self.mousepos[1] / d) * 3

            self.rollcooldown = 10

        if self.rollcooldown > 0:
            self.rollcooldown -= self.ETM * 7

        if not self.stun:
            self.velx += accx * speed * self.ETM
            self.vely += accy * speed * self.ETM

        self.vely *= 0.9
        self.velx *= 0.9

        # if self.vely >= 0 and self.velx >= 0:


        return

    def blockParryDodge(self, screen):
        pygame.draw.rect(screen,(255,0,0),(960 - self.pc , 570, self.pc * 2, 10))
        if self.pc <= 0:
            self.stun = False
        if self.pc <= 10 and self.a[4] and not self.stun:
            self.blocking = True
            self.stun = False
            self.pc += 5 * self.ETM
            rotate_image = pygame.transform.rotate(self.swordimg.copy(), 45)
            screen.blit(rotate_image, rotate_image.get_rect(
                center=(self.swordbox.center[0] + 960 - 32, self.swordbox.center[1] + 540 - 64)))
            return
        if not self.stun and self.pc >= 10:
            self.pc = 10
            cra = pygame.mixer.Sound("stun.mp3")
            pygame.mixer.Sound.play(cra)
            pygame.mixer.music.stop()
            self.stun = True
            self.blocking = False
            return
        if self.stun and self.pc <= 10:
            self.pc -= 5 * self.ETM
        self.blocking = False

        solidx = self.mousepos[0] + 960
        solidy = self.mousepos[1] + 540
        atans = math.atan2(540 - solidy, 960 - solidx)

        angle = (180 / math.pi) * -atans
        rot = pygame.transform.rotate(self.swordimg.copy(), angle + 90)
        addd = 0

        if self.mousebuttons[0]:
            addd = 20

        self.atcbox = rot.get_rect(center=(self.swordbox.center[0] + 960 - 32, self.swordbox.center[1] + 540 - 64 - addd))
        screen.blit(rot, self.atcbox)

    def draw(self, screen):
        screen.blit(self.img, (960 - 32, 540 - 32))

