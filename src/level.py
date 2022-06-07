from ast import List
import itertools
import constants
import pygame
import electron
import sector
import physics
from vec2d import Vec2d
        
class Level:

    def _generate_sector(self, color: pygame.Color, pos: Vec2d):
        # Short Hand for RGB colors
        r, g, b = color.r, color.g, color.b

        # Wall / Floor Detection
        if r == 0 and b == 0:
            if g == 0: return sector.Wall(self, pos)
            if g != 0: return sector.Floor(self, pos)

        # Magnetic Field Detection
        if r == 0: return sector.MField(self, pos, -b * physics.MAX_MAGNETIC_FIELD / 255)
        if b == 0: return sector.MField(self, pos, +r * physics.MAX_MAGNETIC_FIELD / 255)

        # Special Cases
        if g == 255: return sector.Goal(self, pos)
        if g == 100: return sector.OtherStart(self, pos)
        if g == 0: return sector.Start(self, pos)

        # wtf
        print(f"Unknown Color (r: {r}, g: {g}, b: {b})!")
        return sector.Sector(self, pos)
        

    def __init__(self, file: str):
        image = pygame.image.load(file)

        self.size: Vec2d = Vec2d(image.get_width(), image.get_height())

        self.electrons: List[electron.Electron] = []
        self.completed = False

        self.sectors: List(List(sector.Sector)) = [[
            self._generate_sector(image.unmap_rgb(pixel), Vec2d(x, y))
            for y, pixel in enumerate(row)] 
            for x, row in enumerate(pygame.PixelArray(image))]

        self.pixels = pygame.PixelArray(pygame.Surface(tuple(self.size)))

    ### DRAWING ###

    @property
    def surface(self):
        for x, row in enumerate(self.sectors):
            for y, pixel in enumerate(row):
                self.pixels[x, y] = pixel.color

        return self.pixels.make_surface()

    ### FORCES ###

    def get_sector(self, pixel: Vec2d) -> sector.Sector:
        try: return self.sectors[pixel.x][pixel.y]
        except IndexError: return None

    def add_electron(self, electron: electron.Electron):
        self.electrons.append(electron)

    def get_sectors(self, electron: 'electron.Electron'):
        x, y = electron.pos.floor()
        try: yield self.sectors[x + 0][y + 0]
        except IndexError as _e: pass
        try: yield self.sectors[x + 1][y + 0]
        except IndexError as _e: pass
        try: yield self.sectors[x + 0][y + 1]
        except IndexError as _e: pass
        try: yield self.sectors[x - 1][y + 0]
        except IndexError as _e: pass
        try: yield self.sectors[x + 0][y - 1]
        except IndexError as _e: pass
        try: yield self.sectors[x + 1][y + 1]
        except IndexError as _e: pass
        try: yield self.sectors[x + 1][y - 1]
        except IndexError as _e: pass
        try: yield self.sectors[x - 1][y + 1]
        except IndexError as _e: pass
        try: yield self.sectors[x - 1][y - 1]
        except IndexError as _e: pass

    def get_electrons(self):
        return self.electrons

    def get_players(self):
        return filter(lambda e: e.player, self.electrons)

    def get_forces(self, electron: 'electron.Electron'):
        return itertools.chain(self.get_sectors(electron), self.electrons)

    ### SCALING ###

    def pixel_to_screen(self, pixel: Vec2d, board_pos: Vec2d = constants.BOARD_POS, board_size: Vec2d = constants.BOARD_SIZE) -> Vec2d:
        return board_pos + pixel * board_size / self.size

    def screen_to_pixel(self, screen: Vec2d, board_pos: Vec2d = constants.BOARD_POS, board_size: Vec2d = constants.BOARD_SIZE) -> Vec2d:
        return (self.size * (screen - board_pos)) / board_size

    ### NICE TO HAVES ###
    
    def __repr__(self):
        return f"Image(x: {self.size.x}, y:{self.size.y})"
        
    def __str__(self):
        return self.__repr__()