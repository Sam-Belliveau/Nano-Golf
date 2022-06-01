import pygame
from physics import Force
import physics 
import constants

from vec2d import Vec2d


class Electron(Force):

    def __init__(self, pos: Vec2d, player: bool =False):
        self.pos = pos
        self.vel = Vec2d(0, 0)
        self.player = player
        self.charge = physics.ELECTRON_CHARGE

    @property
    def can_shoot(self) -> bool:
        return self.vel.magnitude < constants.MAX_SHOOTING_SPEED

    def magnetic_field(self, pos: Vec2d) -> float:
        r = pos - self.pos
        rm = r.magnitude
        i = physics.ELECTRON_MAGNETIC_FIELD_SCALE * self.charge * self.vel
        return i.cross_vec(r.normalized()) / (rm * rm)

    def apply(self, electron: 'Electron', dt: float) -> None:
        if self == electron: return

        force = self.charge * electron.charge

        distance = self.pos - electron.pos
        r = distance.magnitude

        self.vel += dt * force * distance / (r * r * r)
        self.apply_mfield(electron.magnetic_field(self.pos), dt)

    def apply_mfield(self, force: float, dt: float) -> None:
        self.vel = self.vel.add_cross(dt * self.charge * force)

    def update(self, dt: float) -> None:
        self.pos += self.vel * dt

    @property
    def color(self) -> pygame.Color:
        if self.player: return pygame.Color(255, 255, 255)
        else: return pygame.Color(128, 255, 255)