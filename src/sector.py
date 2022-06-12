import math
import time
import pygame
from vec2d import Vec2d

import level
import electron
import physics
import constants
import colors


class Sector(physics.Force):

    def __init__(self, level: 'level.Level', pos: Vec2d):
        self.level = level
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

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(level, pos)

    @property
    def color(self) -> pygame.Color:
        mag_field = sum((
            electron.magnetic_field(self.center)
            for electron in self.level.get_electrons()
        ))
        return colors.magnetic_field(self.center, mag_field)

    def apply(self, electron: 'electron.Electron', dt: float) -> None:
        if self.contains(electron):
            electron.vel *= math.exp(-dt / constants.FLOOR_FRICTION_DT)
        

class Goal(Floor):

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(level, pos)

    @property
    def color(self) -> pygame.Color: 
        return colors.goal()
    
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        if self.distance(electron.pos).magnitude <= 0.5:
            vel_mag = electron.vel.magnitude
            diff = (self.center - electron.pos)

            if vel_mag < constants.MAX_SCORING_SPEED:
                electron.vel = Vec2d(0, 0)
                electron.pos += diff * (1.0 - math.exp(-dt / 0.5))

                if diff.magnitude < 0.05:
                    self.level.completed = True
            
            else:
                electron.vel = electron.vel.add_cross(
                    dt * diff.cross_vec(electron.vel.normalized()) * constants.HOLE_DEFLECT_SPEED
                ) 


class Start(Floor):

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(level, pos)
        self.level.add_electron(electron.Electron(self.center, player=True))

    @property
    def color(self) -> pygame.Color:
        return colors.start()

    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        super().apply(electron, dt)


class OtherStart(Floor):

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(level, pos)
        self.level = level
        self.level.add_electron(electron.Electron(self.center))

    @property
    def color(self) -> pygame.Color:         
        return colors.start_other()
    
    def apply(self, electron: 'electron.Electron', dt: float) -> None: 
        super().apply(electron, dt)

class MField(Floor): 

    def __init__(self, level: 'level.Level', pos: Vec2d, force: float):
        super().__init__(level, pos)
        self.force = force
        
    @property
    def color(self) -> pygame.Color:
        mag_field = sum((
            electron.magnetic_field(self.center)
            for electron in self.level.get_electrons()
        ))

        return colors.magnetic_field(self.center, mag_field + self.force)
            
    def apply(self, electron: 'electron.Electron', dt: float) -> None:
        super().apply(electron, dt)

        if self.contains(electron):
            electron.apply_mfield(self.force, dt)

class Wall(Sector): 

    def __init__(self, level: 'level.Level', pos: Vec2d):
        super().__init__(level, pos)
        self.t = None
        self.b = None
        self.l = None
        self.r = None

    @property
    def color(self) -> pygame.Color:
        return colors.wall()

    def _update_dirs(self):
        if self.t is None:
            self.t = isinstance(self.level.get_sector(self.pos + Vec2d(+0, +1)), Floor)
            self.b = isinstance(self.level.get_sector(self.pos + Vec2d(+0, -1)), Floor)
            self.l = isinstance(self.level.get_sector(self.pos + Vec2d(-1, +0)), Floor)
            self.r = isinstance(self.level.get_sector(self.pos + Vec2d(+1, +0)), Floor)

    def apply(self, electron: 'electron.Electron', dt: float) -> None:
        dist = self.distance(electron.pos)
        dist_mag = dist.magnitude

        if dist_mag <= 0.5:
            if dist_mag <= 0.0:
                dist = electron.pos - self.center

            self._update_dirs()
            if not self.t: dist.y = min(0.0, dist.y)
            if not self.b: dist.y = max(0.0, dist.y)
            if not self.l: dist.x = max(0.0, dist.x)
            if not self.r: dist.x = min(0.0, dist.x)
            
            normal = dist.normalized()
            electron.vel -= 2.0 * normal * min(0.0, normal.dot(electron.vel))
            
