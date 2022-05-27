from curses import mouseinterval
from typing import Iterable
import constants
import pygame
from electron import Electron

from level import Level
import sector
import physics
from vec2d import Vec2d

class GameState:

    def game_loop(self, dt: float):
        raise NotImplementedError

    def draw(self, screen: pygame.Surface):
        raise NotImplementedError
    
    def is_finished(self) -> bool:
        return False

    def next_state(self) -> Iterable['GameState']:
        pass

class GameLevel:

    def __init__(self, level_num: int):
        self.world = pygame.Rect(*constants.BOARD_POS, *(constants.BOARD_POS + constants.BOARD_SIZE))

        self.level_num = level_num
        self.level = Level(f"./resources/L{level_num}.png")
        self.player = Electron(self.level.start)

        self.ball_size = (constants.BOARD_SIZE / self.level.size).x / 2

        self.mouse_pressed = False
        self.mouse_pos = Vec2d(0, 0)
        self.initial_pos = Vec2d(0, 0)

    def _get_mouse(self) -> Iterable[Vec2d]:
        self.mouse_pos = self.level.screen_to_pixel(Vec2d(*pygame.mouse.get_pos()))

        if pygame.mouse.get_pressed()[0]:
            yield Vec2d(0, 0)
            if not self.mouse_pressed:
                self.initial_pos = self.mouse_pos
                self.mouse_pressed = True
        else:
            if self.mouse_pressed:
                yield (self.initial_pos - self.mouse_pos) * constants.SHOOT_SPEED

            self.mouse_pressed = False
            self.mouse_pos = Vec2d(0, 0)
            self.initial_pos = Vec2d(0, 0)

    def game_loop(self, dt: float):
        
        if self.player.vel.magnitude < constants.MAX_SHOOTING_SPEED:
            for vel in self._get_mouse():
                self.player.vel = vel

        p_dt = dt / physics.PHYSICS_STEPS
        for _i in range(physics.PHYSICS_STEPS):
            self.level.apply(self.player, p_dt)
            self.player.update(p_dt)

    def draw(self, screen: pygame.Surface):
        screen.blit(pygame.transform.scale(self.level.surface, tuple(constants.BOARD_SIZE)), self.world)

        if pygame.mouse.get_pressed()[0]:
            diff = self.mouse_pos - self.initial_pos

            line_start = self.level.pixel_to_screen(self.player.pos)
            line_end = self.level.pixel_to_screen(self.player.pos - diff)
            pygame.draw.line(screen, (255, 0, 0), tuple(line_start), tuple(line_end))


        pygame.draw.circle(screen, (255, 255, 255), tuple(self.level.pixel_to_screen(self.player.pos)), self.ball_size)

    def is_finished(self) -> bool:
        return self.level.completed

    def next_state(self) -> Iterable['GameState']:
        if self.is_finished():
            yield GameLevel(self.level_num + 1)