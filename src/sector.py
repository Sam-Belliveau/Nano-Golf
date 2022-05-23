from ast import List
from electron import Electron
from physics import Force
from vec2d import Vec2d

### PLACEHOLDER ###
class Color: 
    pass


class Sector(Force):

    def __init__(self, pos: Vec2d):
        self.pos = pos

    @property
    def color(self) -> Color: raise NotImplementedError
    
    def apply(self, electron: Electron, dt: float) -> None: raise NotImplementedError


class Floor(Sector): 

    def __init__(self, pos: Vec2d):
        super().__init__(pos)

    @property
    def color(self) -> Color:
        pass

    def apply(self, electron: Electron) -> None:
        # floors don't do anything
        pass
        

class MField(Floor): 

    def __init__(self, pos: Vec2d, force: float):
        super().__init__(pos)
        self.force = force

    @property
    def color(self) -> Color:
        return super().color # modify floor color

    def apply(self, electron: Electron) -> None:
        pass


class Wall(Sector): 

    def __init__(self, pos: Vec2d):
        super().__init__(pos)

    @property
    def color(self) -> Color:
        pass

    def apply(self, electron: Electron) -> None:
        pass
    

### PLACEHOLDER ###
class Image:
    pass

def build_map(image: Image) -> List(List(Sector)):
    pass
