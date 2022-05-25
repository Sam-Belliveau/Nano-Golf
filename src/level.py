import constants
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

        # wtf
        print("somebody made an oopsy")
        return sector.Sector(pos)
        

    def __init__(self, file: str):
        image = pygame.image.load(file)

        self.size: int = Vec2d(image.get_width(), image.get_height())

        self.start: Vec2d = Vec2d(0, 0)

        self.sectors = [[
            self._generate_sector(image.unmap_rgb(pixel), Vec2d(x, y))
            for y, pixel in enumerate(row)] 
            for x, row in enumerate(pygame.PixelArray(image))]

        self.pixels = pygame.PixelArray(pygame.Surface(tuple(self.size)))

    @property
    def surface(self):
        for x, row in enumerate(self.sectors):
            for y, pixel in enumerate(row):
                self.pixels[x, y] = pixel.color

        return self.pixels.make_surface()

    def get_sector(self, pixel: Vec2d) -> sector.Sector:
        return self.sectors[int(pixel.x)][int(pixel.y)]

    def set_sector(self, pixel: Vec2d, sector: sector.Sector):
        sector.pos = pixel
        self.sectors[int(pixel.x)][int(pixel.y)] = sector

    def unit_to_pixel(self, unit: Vec2d) -> Vec2d:
        return unit * self.size / physics.PIXEL_LENGTH

    def pixel_to_unit(self, pixel: Vec2d) -> Vec2d:
        return pixel * physics.PIXEL_LENGTH / self.size

    def pixel_to_screen(self, pixel: Vec2d) -> Vec2d:
        return constants.BOARD_POS + pixel * constants.BOARD_SIZE / self.size

    def screen_to_pixel(self, screen: Vec2d) -> Vec2d:
        return (self.size * (screen - constants.BOARD_POS)) / constants.BOARD_SIZE

    def __repr__(self):
        return f"Image(x: {self.size.x}, y:{self.size.y})"
        
    def __str__(self):
        return self.__repr__()