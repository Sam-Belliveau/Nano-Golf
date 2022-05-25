import constants
import pygame

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
    level = Level("./resources/L1.png")

    pygame.init()

    screen = pygame.display.set_mode([*constants.WINDOW_SIZE])

    world = pygame.Rect(*constants.BOARD_POS, *(constants.BOARD_POS + constants.BOARD_SIZE))

    while game_loop(screen):
        mouse = Vec2d(*pygame.mouse.get_pos())
        mouse = level.screen_to_pixel(mouse)
        level.set_sector(mouse, sector.Wall((0,0)))
        screen.blit(pygame.transform.scale(level.surface, tuple(constants.BOARD_SIZE)), world)
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()