import os
import pygame
import sector
import physics
from vec2d import Vec2d


def get_sector(color: pygame.Color, pos: Vec2d):
    r, g, b = color.r, color.g, color.b
    if r == 0 and b == 0:
        if g == 0:
            return sector.Wall(pos)
        else:
            return sector.Floor(pos)

    if color.r == 0:
        return sector.MField(pos, +r * physics.MAX_MAGNETIC_FIELD / 255)

    if color.b == 0:
        return sector.MField(pos, -r * physics.MAX_MAGNETIC_FIELD / 255)

    return sector.Sector(pos)
        

class Level:

    def __init__(self, file: str):
        image = pygame.image.load(file)

        self.width = image.get_width()
        self.height = image.get_height()

        self.sectors = [
            [
                get_sector(pygame.Color(pixel), Vec2d(x, y))
                for x, pixel
                in enumerate(row)
            ] 
            for y, row 
            in enumerate(pygame.PixelArray(image))
        ]



    def __repr__(self):
        return f"Image(x: {self.width}, y:{self.height})"
        
    def __str__(self):
        return self.__repr__()