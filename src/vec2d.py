from __future__ import annotations

class Vec2d:

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y


    ### ADD ###

    def __add__(self, rhs: Vec2d) -> Vec2d:
        return Vec2d(
            self.x + rhs.x, 
            self.y + rhs.y
        )

    def __iadd__(self, rhs: Vec2d) -> Vec2d:
        self.x += rhs.x 
        self.y += rhs.y


    ### SUB ###

    def __sub__(self, rhs: Vec2d) -> Vec2d:
        return Vec2d(
            self.x - rhs.x, 
            self.y - rhs.y
        )

    def __isub__(self, rhs: Vec2d) -> None:
        self.x -= rhs.x 
        self.y -= rhs.y


    ### MUL ###

    def __mul__(self, rhs: float) -> Vec2d:
        return Vec2d(
            self.x * rhs, 
            self.y * rhs
        )

    def __rmul__(self, rhs: float) -> Vec2d:
        return Vec2d(
            self.x * rhs, 
            self.y * rhs
        )

    def __imul__(self, rhs: float) -> None:
        self.x *= rhs
        self.y *= rhs


    ### DIV ###

    def __truediv__(self, rhs: float) -> Vec2d:
        return Vec2d(
            self.x / rhs, 
            self.y / rhs
        )

    def __itruediv__(self, rhs: float) -> None:
        self.x /= rhs
        self.y /= rhs

    ### Products ###

    def dot(self, rhs: Vec2d) -> float:
        return self.x * rhs.x + self.y * rhs.y

    def cross(self, z: float) -> Vec2d:
        return Vec2d(
            +self.y * z,
            -self.x * z
        )

    ### Nice To Haves ###

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vec2d(x: {self.x}, y:{self.y})"
        

