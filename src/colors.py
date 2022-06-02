import math
from pygame import Color
from time import time
from math import sin

from vec2d import Vec2d
import physics

def clamp(c: float):
    if c <= 0.000: return 0
    if c >= 255.0: return 255
    return int(c)

def average_sin(freq: float = 1.0, phase: float = 0.0):
    return (sin(freq * time() + phase) + 1.0) * 0.5 

def average_colors(a: Color, b: Color, t: float):
    GAMMA = 2.22
    INV_GAMMA = 1.0 / GAMMA

    if t <= 0.0: return a
    if t >= 1.0: return b

    a = a.correct_gamma(GAMMA)
    b = b.correct_gamma(GAMMA)
    
    return Color(
        clamp((1.0 - t) * a.r + (t) * b.r),
        clamp((1.0 - t) * a.g + (t) * b.g),
        clamp((1.0 - t) * a.b + (t) * b.b),
        clamp((1.0 - t) * a.a + (t) * b.a)
    ).correct_gamma(INV_GAMMA)

def wall():
    return Color(24, 0, 24)

def floor():
    return Color(0, 200, 0)

def start():
    return Color(0, 120, 0)

def start_other():
    return Color(0, 160, 0)

def goal():
    BRIGHT = Color(255, 64, 255)
    DARK = Color(192, 0, 192)

    return average_colors(BRIGHT, DARK, average_sin(5))

def magnetic_field(pos: Vec2d, strength):
    POSITIVE_DARK_COLOR = Color(200, 0, 0)
    POSITIVE_BRIGHT_COLOR = Color(255, 0, 48)
    NEGATIVE_DARK_COLOR = Color(0, 0, 200)
    NEGATIVE_BRIGHT_COLOR = Color(48, 0, 255)

    strength /= physics.MAX_MAGNETIC_FIELD
    t = abs(strength)

    if 0 < strength: 
        positive_color = average_colors(
            POSITIVE_BRIGHT_COLOR,
            POSITIVE_DARK_COLOR,
            average_sin(-12, 0.5 * math.pi * pos.y)
        )
        return average_colors(floor(), positive_color, t)

    if 0 > strength:
        negative_color = average_colors(
            NEGATIVE_BRIGHT_COLOR,
            NEGATIVE_DARK_COLOR,
            average_sin(12, 0.5 * math.pi * pos.y)
        )
        return average_colors(floor(), negative_color, t)

    return floor()
