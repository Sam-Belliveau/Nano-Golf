import pygame
import random
from vec2d import Vec2d

import level
import electron
import physics


class Sector(physics.Force):

    def __init__(self, pos: Vec2d):
        self.pos = pos

    @property
    def color(self) -> pygame.Color: 
        raise NotImplementedError
    
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        raise NotImplementedError


class Floor(Sector): 

    def __init__(self, pos: Vec2d):
        super().__init__(pos)

    @property
    def color(self) -> pygame.Color:
        return pygame.Color(0, 255, 0)

    def apply(self, electron: 'electron.Electron', dt: float) -> None:
        # floors don't do anything
        pass
        

class Goal(Floor):

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(pos)
        self.level = level

    @property
    def color(self) -> pygame.Color: 
        return pygame.Color(random.randint(128, 255), 255, random.randint(128, 255))
    
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        super().apply(electron, dt)


class Start(Floor):

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(pos)
        self.level = level
        self.level.start = self.pos

    @property
    def color(self) -> pygame.Color: 
        return pygame.Color(0, 120, 0)
    
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        super().apply(electron, dt)


class MField(Floor): 

    def __init__(self, pos: Vec2d, force: float):
        super().__init__(pos)
        self.force = force

    @property
    def color(self) -> pygame.Color:
        r = max(0, min(255, 
            self.force * 255 / physics.MAX_MAGNETIC_FIELD
        ))
        b = max(0, min(255, 
            -self.force * 255 / physics.MAX_MAGNETIC_FIELD
        ))
        
        return pygame.Color(r, 255 - r - b, b)

    def apply(self, electron: 'electron.Electron', dt: float) -> None:
        super().apply(electron, dt)


class Wall(Sector): 

    def __init__(self, pos: Vec2d):
        super().__init__(pos)

    @property
    def color(self) -> pygame.Color:
        return pygame.Color(0, 0, 0)

    def apply(self, electron: 'electron.Electron', dt: float) -> None:
        pass
