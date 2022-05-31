from math import dist
from physics import Force
import physics 

from vec2d import Vec2d


class Electron(Force):

    def __init__(self, pos: Vec2d):
        self.pos = pos
        self.vel = Vec2d(0, 0)
        self.charge = physics.ELECTRON_CHARGE

    def apply(self, electron: 'Electron', dt: float) -> None:
        if self == electron: return

        force = self.charge * electron.charge

        distance = self.pos - electron.pos
        r = distance.magnitude

        self.vel += dt * force * distance.normalized() / (r * r)

    def apply_mfield(self, force: float, dt: float):
        self.vel = self.vel.add_cross(self.charge * dt * force)

    def update(self, dt: float):
        self.pos += self.vel * dt