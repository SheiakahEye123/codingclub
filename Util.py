import pygame

class Util():
    def rotate(self, center, img, angle):
        rotimg = pygame.transform.rotate(img,angle)
        box = rotimg.get_rect()
        box.center = center

        return rotimg

