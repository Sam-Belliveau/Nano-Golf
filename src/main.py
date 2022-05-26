import constants
import pygame
from electron import Electron

from level import Level
import sector
from vec2d import Vec2d

def game_loop(screen) -> bool:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    # Fill the background with white
    screen.fill((255, 255, 255))

    return True


def main():
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([*constants.WINDOW_SIZE])

    world = pygame.Rect(*constants.BOARD_POS, *(constants.BOARD_POS + constants.BOARD_SIZE))

    level = Level("./resources/L1.png")
    electron = Electron(level.start)
    electron.vel.x = 25

    while game_loop(screen):
        dt = clock.tick(60) / 1000.0

        level.apply(electron, dt)
        electron.update(dt)

        screen.blit(pygame.transform.scale(level.surface, tuple(constants.BOARD_SIZE)), world)
        pygame.draw.circle(screen, (255, 255, 255), tuple(level.pixel_to_screen(electron.pos)), 10)
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()