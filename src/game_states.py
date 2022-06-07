
from typing import Iterable
import constants
import pygame

from level import Level
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

class GameLevel(GameState):

    def __init__(self, level_num: int, shots: int=0):
        self.world = pygame.Rect(*constants.BOARD_POS, *(constants.BOARD_POS + constants.BOARD_SIZE))

        self.level_num = level_num
        self.level = Level(f"./resources/L{level_num}.png")

        self.ball_size = (constants.BOARD_SIZE / self.level.size).x / 2

        self.mouse_pressed = False
        self.mouse_pos = Vec2d(0, 0)
        self.initial_pos = Vec2d(0, 0)

        self.shots = 0
        self.total_shots = shots

        self.cheating = False

    def _is_cheating(self) -> bool:
        k = pygame.key.get_pressed()
        pressed = k[pygame.K_n] and k[pygame.K_e] and k[pygame.K_x] and k[pygame.K_t]

        if self.cheating and not pressed:
            self.cheating = False
            return True
        elif pressed:
            self.cheating = True

    def _get_mouse(self) -> Iterable[Vec2d]:
        self.mouse_pos = self.level.screen_to_pixel(Vec2d(*pygame.mouse.get_pos()))

        if pygame.mouse.get_pressed()[0]:
            yield Vec2d(0, 0)
            if not self.mouse_pressed:
                self.initial_pos = self.mouse_pos
                self.mouse_pressed = True
        else:
            if self.mouse_pressed:
                self.shots += 1
                self.total_shots += 1
                yield (self.initial_pos - self.mouse_pos).cap_magnitude(constants.SHOOT_SPEED_CAP) * constants.SHOOT_SPEED

            self.mouse_pressed = False
            self.mouse_pos = Vec2d(0, 0)
            self.initial_pos = Vec2d(0, 0)

    def game_loop(self, dt: float):
        for vel in self._get_mouse():
            for player in self.level.get_players():
                if player.can_shoot:
                        player.vel += vel

        p_dt = dt / physics.SUBSTEPS
        for _i in range(physics.SUBSTEPS):
            for electron in self.level.get_electrons():
                for force in self.level.get_forces(electron):
                    force.apply(electron, p_dt)

            for electron in self.level.get_electrons():
                electron.update(p_dt)

        if self._is_cheating():
            self.total_shots += 1000
            self.level.completed = True


    def draw(self, screen: pygame.Surface):
        screen.fill(pygame.Color(24, 64, 24))
        screen.blit(pygame.transform.scale(self.level.surface, tuple(constants.BOARD_SIZE)), self.world)

        title = constants.FONT_BIG.render('Nano-Golf', True, (255, 255, 255))
        level = constants.FONT_NORMAL.render(f"Level: #{self.level_num}", True, (255, 255, 255))
        score = constants.FONT_NORMAL.render(f"Score: {self.total_shots}", True, (255, 255, 255))
        shots = constants.FONT_NORMAL.render(f"Strokes: {self.shots}", True, (255, 255, 255))

        screen.blit(title, (550, 60))
        screen.blit(level, (560, 120))
        screen.blit(score, (560, 160))
        screen.blit(shots, (560, 200))

        if pygame.mouse.get_pressed()[0]:
            diff = (self.mouse_pos - self.initial_pos).cap_magnitude(constants.SHOOT_SPEED_CAP)

            for player in self.level.get_players():
                if player.can_shoot:
                    line_start = self.level.pixel_to_screen(player.pos)
                    line_end = self.level.pixel_to_screen(player.pos - diff)
                    pygame.draw.line(screen, (255, 0, 0), tuple(line_start), tuple(line_end))

        for electron in self.level.get_electrons():
            pygame.draw.circle(screen, electron.color, tuple(self.level.pixel_to_screen(electron.pos)), self.ball_size)

    def is_finished(self) -> bool:
        return self.level.completed

    def next_state(self) -> Iterable['GameState']:
        if self.is_finished():
            try:
                yield GameLevel(self.level_num + 1, self.total_shots)
            except Exception as _e:
                yield EndScreen(self.total_shots)


class StartMenu(GameState):

    def __init__(self):
        self.world = pygame.Rect(0, 0, *constants.WINDOW_SIZE)

        self.level = Level(f"./resources/MENU.png")

        self.ball_size = (constants.WINDOW_SIZE / self.level.size).x / 2

        self.mouse_pressed = False
        self.mouse_pos = Vec2d(0, 0)
        self.initial_pos = Vec2d(0, 0)

    def _get_mouse(self) -> Iterable[Vec2d]:
        self.mouse_pos = self.level.screen_to_pixel(Vec2d(*pygame.mouse.get_pos()), Vec2d(0, 0), constants.WINDOW_SIZE)

        if pygame.mouse.get_pressed()[0]:
            yield Vec2d(0, 0)
            if not self.mouse_pressed:
                self.initial_pos = self.mouse_pos
                self.mouse_pressed = True
        else:
            if self.mouse_pressed:
                yield (self.initial_pos - self.mouse_pos).cap_magnitude(constants.SHOOT_SPEED_CAP / 2) * constants.SHOOT_SPEED

            self.mouse_pressed = False
            self.mouse_pos = Vec2d(0, 0)
            self.initial_pos = Vec2d(0, 0)

    def game_loop(self, dt: float):
        for vel in self._get_mouse():
            for player in self.level.get_players():
                if player.can_shoot:
                        player.vel += vel

        p_dt = dt / physics.SUBSTEPS
        for _i in range(physics.SUBSTEPS):
            for electron in self.level.get_electrons():
                for force in self.level.get_forces(electron):
                    force.apply(electron, p_dt)

            for electron in self.level.get_electrons():
                electron.update(p_dt)

    def draw(self, screen: pygame.Surface):
        screen.fill(pygame.Color(24, 64, 24))
        screen.blit(pygame.transform.scale(self.level.surface, tuple(constants.WINDOW_SIZE)), self.world)

        instruction = constants.FONT_NORMAL.render(f"Click & Drag to Start", True, (255, 255, 255))
        author = constants.FONT_NORMAL.render(f"By: Ayan & Sam", True, (255, 255, 255))

        screen.blit(instruction, (300, 380))
        screen.blit(author, (320, 260))

        if pygame.mouse.get_pressed()[0]:
            diff = (self.mouse_pos - self.initial_pos).cap_magnitude(constants.SHOOT_SPEED_CAP / 2)

            for player in self.level.get_players():
                if player.can_shoot:
                    line_start = self.level.pixel_to_screen(player.pos, Vec2d(0, 0), constants.WINDOW_SIZE)
                    line_end = self.level.pixel_to_screen(player.pos - diff, Vec2d(0, 0), constants.WINDOW_SIZE)
                    pygame.draw.line(screen, (255, 0, 0), tuple(line_start), tuple(line_end))

        for electron in self.level.get_electrons():
            pygame.draw.circle(screen, electron.color, tuple(self.level.pixel_to_screen(electron.pos, Vec2d(0, 0), constants.WINDOW_SIZE)), self.ball_size)

    def is_finished(self) -> bool:
        return self.level.completed

    def next_state(self) -> Iterable['GameState']:
        if self.is_finished():
            try:
                yield GameLevel(1)
            except Exception as _e:
                yield EndScreen(self.total_shots)

class EndScreen(StartMenu):

    def __init__(self, score: int):
        super().__init__()
        self.final_score = score

    def draw(self, screen: pygame.Surface):
        screen.fill(pygame.Color(24, 64, 24))
        screen.blit(pygame.transform.scale(self.level.surface, tuple(constants.WINDOW_SIZE)), self.world)

        instruction = constants.FONT_NORMAL.render(f"Click & Drag to Restart", True, (255, 255, 255))
        score = constants.FONT_NORMAL.render(f"Final Score: {self.final_score}", True, (255, 255, 255))

        screen.blit(instruction, (290, 380))
        screen.blit(score, (320, 260))

        if pygame.mouse.get_pressed()[0]:
            diff = (self.mouse_pos - self.initial_pos).cap_magnitude(constants.SHOOT_SPEED_CAP / 2)

            for player in self.level.get_players():
                if player.can_shoot:
                    line_start = self.level.pixel_to_screen(player.pos, Vec2d(0, 0), constants.WINDOW_SIZE)
                    line_end = self.level.pixel_to_screen(player.pos - diff, Vec2d(0, 0), constants.WINDOW_SIZE)
                    pygame.draw.line(screen, (255, 0, 0), tuple(line_start), tuple(line_end))

        for electron in self.level.get_electrons():
            pygame.draw.circle(screen, electron.color, tuple(self.level.pixel_to_screen(electron.pos, Vec2d(0, 0), constants.WINDOW_SIZE)), self.ball_size)

    def is_finished(self) -> bool:
        return self.level.completed

    def next_state(self) -> Iterable['GameState']:
        if self.is_finished():
            try:
                yield GameLevel(1)
            except Exception as _e:
                yield EndScreen(self.total_shots)
