from math import dist

import pygame
from physics import Force
import physics 

from vec2d import Vec2d


class Electron(Force):

    def __init__(self, pos: Vec2d, player=False):
        self.pos = pos
        self.vel = Vec2d(0, 0)
        self.player = player
        self.charge = physics.ELECTRON_CHARGE

    def substeps(self, dt: float) -> int:
        return max(1, int(self.vel.magnitude * dt / physics.MAX_STEP_SIZE))

    def apply(self, electron: 'Electron', dt: float) -> None:
        if self == electron: return

        force = self.charge * electron.charge

        distance = self.pos - electron.pos
        r = distance.magnitude

        self.vel += dt * force * distance.normalized() / (r * r)

    def apply_mfield(self, force: float, dt: float) -> None:
        self.vel = self.vel.add_cross(self.charge * dt * force)

    def update(self, dt: float) -> None:
        self.pos += self.vel * dt

    @property
    def color(self) -> pygame.Color:
        if self.player: return pygame.Color(255, 255, 255)
        else: return pygame.Color(128, 200, 255)