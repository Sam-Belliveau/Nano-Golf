from physics import Force

from vec2d import Vec2d


class Electron(Force):

    def __init__(self, pos: Vec2d):
        self.pos = pos
        self.vel = Vec2d()

    def apply(self, electron: 'Electron', dt: float) -> None:
        # TODO:
        pass