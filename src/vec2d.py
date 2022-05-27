from __future__ import annotations
import math
from re import X

class Vec2d:

    def __init__(self, x: float | int = 0.0, y: float | int = 0.0):
        self.x = x
        self.y = y


    ### ADD ###

    def __add__(self, rhs: Vec2d) -> Vec2d:
        return Vec2d(
            self.x + rhs.x, 
            self.y + rhs.y
        )


    ### SUB ###

    def __sub__(self, rhs: Vec2d) -> Vec2d:
        return Vec2d(
            self.x - rhs.x, 
            self.y - rhs.y
        )

    ### MUL ###

    def __mul__(self, rhs: float | int | Vec2d) -> Vec2d:
        if isinstance(rhs, (float, int)):
            return Vec2d(
                self.x * rhs, 
                self.y * rhs
            )
        
        if isinstance(rhs, Vec2d):
            return Vec2d(
                self.x * rhs.x, 
                self.y * rhs.y
            )

    def __rmul__(self, rhs: float | int | Vec2d) -> Vec2d:
        if isinstance(rhs, (float, int)):
            return Vec2d(
                self.x * rhs, 
                self.y * rhs
            )
        
        if isinstance(rhs, Vec2d):
            return Vec2d(
                self.x * rhs.x, 
                self.y * rhs.y
            )


    ### DIV ###

    def __truediv__(self, rhs: float | int) -> Vec2d:
        if isinstance(rhs, (float, int)):
            return Vec2d(
                self.x / rhs, 
                self.y / rhs
            )
        
        if isinstance(rhs, Vec2d):
            return Vec2d(
                self.x / rhs.x, 
                self.y / rhs.y
            )

    ### Products ###

    def dot(self, rhs: Vec2d) -> float:
        return self.x * rhs.x + self.y * rhs.y

    def cross(self, z: float) -> Vec2d:
        return Vec2d(
            +self.y * z,
            -self.x * z
        )

    ### Nice To Haves ###

    @property
    def magnitude(self) -> float:
        return math.hypot(self.x, self.y)

    def floor(self) -> Vec2d:
        return Vec2d(
            int(self.x),
            int(self.y)
        )

    def __iter__(self):
        yield self.x
        yield self.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vec2d(x: {self.x}, y:{self.y})"

    def __eq__(self, rhs: Vec2d) -> bool:
        return self.x == rhs.x and self.y == rhs.y

    def __ne__(self, rhs: Vec2d) -> bool:
        return self.x != rhs.x or self.y != rhs.y
        

