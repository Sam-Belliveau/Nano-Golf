import math
import time
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

    def contains(self, electron: 'electron.Electron') -> bool:
        return self.pos == electron.pos.floor()
    
    def contains_radius(self, electron: 'electron.Electron', radius: float = 0.0):
        dp = electron.pos - self.pos
        return ((-radius <= dp.x) and (dp.x <= radius + 1)
            and (-radius <= dp.y) and (dp.y <= radius + 1))
        


class Floor(Sector): 

    def __init__(self, pos: Vec2d):
        super().__init__(pos)

    @property
    def color(self) -> pygame.Color:
        return pygame.Color(0, 200, 0)

    def apply(self, electron: 'electron.Electron', dt: float) -> None:
        if self.contains(electron):
            electron.vel *= math.exp(-dt / constants.FLOOR_FRICTION_DT)
        

class Goal(Floor):

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(pos)
        self.center = self.pos + Vec2d(0.5, 0.5)
        self.level = level

    @property
    def color(self) -> pygame.Color: 
        s = int(30 * math.sin(12 * time.time()))
        y = int(224 + s)
        return pygame.Color(y, 32 + s, y)
    
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        if self.contains(electron):
            vel_mag = electron.vel.magnitude
            diff = (self.center - electron.pos)

            if vel_mag < constants.MAX_SCORING_SPEED:
                m = 1.0 - math.exp(-dt / 0.5)

                electron.vel = Vec2d(0, 0)
                electron.pos += diff * m

                if diff.magnitude < 0.05:
                    self.level.completed = True
            
            else:
                electron.vel = electron.vel.add_cross(
                    dt * diff.cross_vec(electron.vel) * constants.HOLE_DEFLECT_SPEED
                ) 


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
        
        self.r = int(max(0, min(255, 
            +self.force * 255 / physics.MAX_MAGNETIC_FIELD
        )))
        self.b = int(max(0, min(255, 
            -self.force * 255 / physics.MAX_MAGNETIC_FIELD
        )))
        self.g = int(max(0, min(255, 64 - self.r - self.b)))

    @property
    def color(self) -> pygame.Color:
        return pygame.Color(self.r, self.g, self.b)

    def apply(self, electron: 'electron.Electron', dt: float) -> None:
        super().apply(electron, dt)

        if self.contains(electron):
            electron.vel = electron.vel.add_cross(-dt * self.force)


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

        if self.contains_radius(electron, 0.5):
            rel_pos = electron.pos - self.pos

            t, b, l, r = self._get_dirs()

            t &= rel_pos.y >= 0.5
            b &= rel_pos.y <= 0.5
            l &= rel_pos.x <= 0.5
            r &= rel_pos.y >= 0.5

            t &= electron.vel.y <= 0.0
            b &= electron.vel.y >= 0.0
            l &= electron.vel.x >= 0.0
            r &= electron.vel.x <= 0.0
            
            if (t and r) or (b and l):
                electron.vel = Vec2d(-electron.vel.y, -electron.vel.x)  

            elif (t and l) or (b and r):
                electron.vel = Vec2d(electron.vel.y, electron.vel.x)  

            elif t or b: 
                electron.vel.y *= -1
                
            elif l or r: 
                electron.vel.x *= -1
            
            
