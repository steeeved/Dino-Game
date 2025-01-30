import pygame
from pygame import *


def load_sprite_sheet(
        s_name,
        namex,
        namey,
        scx=-1,
        scy=-1,
        c_key=None,
):
    fullname = os.path.join('resources', s_name)
    sh = pygame.image.load(fullname)
    sh = sh.convert()

    sh_rect = sh.get_rect()

    sprites = []

    sx = sh_rect.width / namex
    sy = sh_rect.height / namey

    for i in range(0, namey):
        for j in range(0, namex):
            rect = pygame.Rect((j*sx, i*sy, sx, sy))
            img = pygame.Surface(rect.size)
            img = img.convert()
            img.blit(sh, (0, 0), rect)

            if c_key is not None:
                if c_key == -1:
                    c_key = img.get_at((0, 0))
                img.set_colorkey(c_key, RLEACCEL)

            if scx != -1 or scy != -1:
                img = pygame.transform.scale(img, (scx, scy))

            sprites.append(img)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect

def load_image(
    name,
    sx=-1,
    sy=-1,
    colorkey=None,
):
    fullname = os.path.join('resources', name)
    img = pygame.image.load(fullname)
    img = img.convert()
    
    # this code sets a transparent color for the img Surface.
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        # RLEACCEL flag to optimize blitting.
        img.set_colorkey(colorkey, RLEACCEL)

    if sx != -1 or sy != -1:
        img = pygame.transform.scale(img, (sx, sy))

    return (img, img.get_rect())

def extractDigits(num):
    if num > -1:
        d = []
        i = 0
        while(num / 10 != 0):
            d.append(num % 10)
            num = int(num / 10)

        d.append(num % 10)
        for i in range(len(d),5):
            d.append(0)
        d.reverse()
        return d