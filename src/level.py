import os
import pygame
import sector
import physics
from vec2d import Vec2d
        
class Level:

    def _generate_sector(self, color: pygame.Color, pos: Vec2d):
        # Short Hand for RGB colors
        r, g, b = color.r, color.g, color.b

        # Wall / Floor Detection
        if r == 0 and b == 0:
            if g == 0: return sector.Wall(pos)
            if g != 0: return sector.Floor(pos)

        # Magnetic Field Detection
        if r == 0: return sector.MField(pos, -b * physics.MAX_MAGNETIC_FIELD / 255)
        if b == 0: return sector.MField(pos, +r * physics.MAX_MAGNETIC_FIELD / 255)

        # Special Cases
        if g >= 128: return sector.Goal(self, pos)
        if g <= 127: return sector.Start(self, pos)

        return sector.Sector(pos)
        

    def __init__(self, file: str):
        image = pygame.image.load(file)

        self.width: int = image.get_width()
        self.height: int = image.get_height()

        self.start: Vec2d = Vec2d(0, 0)

        self.sectors = [[
            self._generate_sector(image.unmap_rgb(pixel), Vec2d(x, y))
            for y, pixel in enumerate(row)] 
            for x, row in enumerate(pygame.PixelArray(image))]

    @property
    def surface(self):
        pixels = pygame.PixelArray(pygame.Surface((self.width, self.height)))

        for x, row in enumerate(self.sectors):
            for y, pixel in enumerate(row):
                pixels[x, y] = pixel.color

        return pixels.make_surface()
            


    def __repr__(self):
        return f"Image(x: {self.width}, y:{self.height})"
        
    def __str__(self):
        return self.__repr__()