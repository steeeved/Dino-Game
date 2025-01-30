import pygame
from  modules.helpers import load_sprite_sheet, extractDigits

screenDisplay = (width_screen, height_screen) = (600, 400)
backgroundColor = (235, 235, 235)

class Scoreboard():
    def __init__(self,x=-1,y=-1):
        self.score = 0
        self.scre_img, self.screrect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
        self.image = pygame.Surface((55,int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width_screen * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height_screen * 0.1
        else:
            self.rect.top = y

    def draw(self):
        screenDisplay.blit(self.image, self.rect)

    def update(self,score):
        score_digits = extractDigits(score)
        self.image.fill(backgroundColor)
        for s in score_digits:
            self.image.blit(self.scre_img[s], self.screrect)
            self.screrect.left += self.screrect.width
        self.screrect.left = 0