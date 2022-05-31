import math
import time
import pygame
from vec2d import Vec2d

import level
import electron
import physics
import constants


class Sector(physics.Force):

    def __init__(self, pos: Vec2d):
        self.pos = pos.floor()
        self.center = self.pos + Vec2d(0.5, 0.5)

    @property
    def color(self) -> pygame.Color: 
        raise NotImplementedError
    
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        raise NotImplementedError

    def distance(self, pos: Vec2d) -> Vec2d:
        dp = pos - self.center
        return Vec2d(
            min(0.0, dp.x + 0.5) + max(0.0, dp.x - 0.5),
            min(0.0, dp.y + 0.5) + max(0.0, dp.y - 0.5),
        )

    def contains(self, electron: 'electron.Electron') -> bool:
        return self.pos == electron.pos.floor()
        

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
        self.level = level

    @property
    def color(self) -> pygame.Color: 
        s = int(30 * math.sin(12 * time.time()))
        y = int(224 + s)
        return pygame.Color(y, 32 + s, y)
    
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        if self.distance(electron.pos).magnitude <= 0.5:
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
        
    @property
    def color(self) -> pygame.Color:
        color = super().color
        if 0 < self.force:
            color.r = int(160 + 32 * math.sin(self.pos.y + self.force * time.time()))
            color.g = color.g - color.r

        if 0 > self.force:
            color.b = int(160 + 32 * math.sin(self.pos.y + self.force * time.time()))
            color.g = color.g - color.b

        return color
            

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
        dist = self.distance(electron.pos)

        if dist.magnitude <= 0.5:
            t, b, l, r = self._get_dirs()
            t &= dist.y >= 0.0
            b &= dist.y <= 0.0
            l &= dist.x <= 0.0
            r &= dist.x >= 0.0

            if not t: dist.y = min(0.0, dist.y)
            if not b: dist.y = max(0.0, dist.y)
            if not l: dist.x = max(0.0, dist.x)
            if not r: dist.x = min(0.0, dist.x)
            
            normal = dist.normalized()
            electron.vel -= 2.0 * normal * min(0.0, normal.dot(electron.vel))
            
