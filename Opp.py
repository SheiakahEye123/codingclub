import pygame

class Opp():
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.sword = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("sword.png"), (64, 64)), 45)
        self.img = pygame.transform.scale(pygame.image.load("knight.png"), (64,64))
        self.ETM = 0
        self.velx = 0
        self.vely = 0
        self.health = 100

    def accelerate(self, speed):
        accx = 0
        accy = 0
        if self.player.y * 64 <= self.y * 64:
            # w
            accy += -1
        if self.player.x * 64 <= self.x * 64:
            # a
            accx += -1
        if self.player.y * 64 >= self.y * 64:
            # s
            accy += 1
        if self.player.x * 64 >= self.x * 64:
            # d
            accx += 1

        self.velx += accx * speed * self.ETM
        self.vely += accy * speed * self.ETM

        self.vely *= 0.9
        self.velx *= 0.9

        # if self.vely >= 0 and self.velx >= 0:
        return

    def draw(self, screen):
        pygame.draw.rect(screen, (0,255,0), (((self.x-self.player.x) * 64 + 960),((self.y-self.player.y) * 64 + 540),64,64))





