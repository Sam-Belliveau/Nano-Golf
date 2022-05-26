import math
import pygame
import random
from vec2d import Vec2d

import level
import electron
import physics
import constants


class Sector(physics.Force):

    def __init__(self, pos: Vec2d):
        self.pos = pos.floor()

    @property
    def color(self) -> pygame.Color: 
        raise NotImplementedError
    
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        raise NotImplementedError

    def contains(self, electron: 'electron.Electron', radius = 0.0) -> bool:
        if radius == 0.0:
            return self.pos == electron.pos.floor()
        
        dp = electron.pos - self.pos
        return ((-radius <= dp.x) or (dp.x <= radius + 1)
             or (-radius <= dp.y) or (dp.y <= radius + 1))
        


class Floor(Sector): 

    def __init__(self, pos: Vec2d):
        super().__init__(pos)

    @property
    def color(self) -> pygame.Color:
        return pygame.Color(0, 255, 0)

    def apply(self, electron: 'electron.Electron', dt: float) -> None:
        print(f"pos: {electron.pos}")
        print(f"vel: {electron.vel}")
        if self.contains(electron):
            electron.vel *= math.exp(-dt / constants.FLOOR_FRICTION_DT)
        

class Goal(Floor):

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(pos)
        self.level = level

    @property
    def color(self) -> pygame.Color: 
        return pygame.Color(random.randint(128, 255), 255, random.randint(128, 255))
    
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        super().apply(electron, dt)

        if self.contains(electron):
            # win condition
            pass


class Start(Floor):

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(pos)
        self.level = level
        self.level.start = self.pos + Vec2d(0.5, 0.5)

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

        if self.contains(electron):
            electron.vel -= dt * electron.vel.cross(self.force)


class Wall(Sector): 

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(pos)
        self.level = level
        self.t = None
        self.b = None
        self.l = None
        self.r = None

    @property
    def color(self) -> pygame.Color:
        return pygame.Color(0, 0, 0)

    def _get_dirs(self):
        if self.t is None:
            self.t = isinstance(self.level.get_sector(self.pos + Vec2d(+0, +1)), Floor)
            self.b = isinstance(self.level.get_sector(self.pos + Vec2d(+0, -1)), Floor)
            self.l = isinstance(self.level.get_sector(self.pos + Vec2d(-1, +0)), Floor)
            self.r = isinstance(self.level.get_sector(self.pos + Vec2d(+1, +0)), Floor)

        return self.t, self.b, self.l, self.r

    def apply(self, electron: 'electron.Electron', dt: float) -> None:

        if self.contains(electron, 1.0):
            rel_pos = electron.pos - self.pos

            t, b, l, r = self._get_dirs()

            t &= rel_pos.y >= 0.5
            b &= rel_pos.y <= 0.5
            l &= rel_pos.x <= 0.5
            r &= rel_pos.y >= 0.5

            t &= electron.vel.y <= 0
            b &= electron.vel.y >= 0
            l &= electron.vel.x >= 0
            r &= electron.vel.x <= 0

            if t or b: electron.vel.y *= -1
            if l or r: electron.vel.x *= -1
            
