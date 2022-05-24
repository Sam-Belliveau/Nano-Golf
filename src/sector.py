from ast import List
from vec2d import Vec2d

import electron
import physics

### PLACEHOLDER ###
class Color: 
    pass


class Sector(physics.Force):

    def __init__(self, pos: Vec2d):
        self.pos = pos

    @property
    def color(self) -> Color: 
        raise NotImplementedError
    
    def apply(self, electron: electron.Electron, dt: float) -> None: 
        raise NotImplementedError


class Floor(Sector): 

    def __init__(self, pos: Vec2d):
        super().__init__(pos)

    @property
    def color(self) -> Color:
        pass

    def apply(self, electron: electron.Electron) -> None:
        # floors don't do anything
        pass
        

class MField(Floor): 

    def __init__(self, pos: Vec2d, force: float):
        super().__init__(pos)
        self.force = force

    @property
    def color(self) -> Color:
        return super().color # modify floor color

    def apply(self, electron: electron.Electron) -> None:
        pass


class Wall(Sector): 

    def __init__(self, pos: Vec2d):
        super().__init__(pos)

    @property
    def color(self) -> Color:
        pass

    def apply(self, electron: electron.Electron) -> None:
        pass
