import constants
import pygame
from electron import Electron
from game_states import GameLevel, StartMenu

from level import Level
import sector
import physics
from vec2d import Vec2d

def pygame_running(screen) -> bool:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    # Fill the background with white
    screen.fill((255, 255, 255))

    return True


def main():
    pygame.init()
    constants.FONT_BIG = pygame.font.SysFont("arial.ttf", 60, bold=True)
    constants.FONT_NORMAL = pygame.font.SysFont("arial.ttf", 32)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([*constants.WINDOW_SIZE])
    pygame.display.set_icon(pygame.image.load("./resources/icon.png"))
    pygame.display.set_caption("Nano-Golf - Ayan & Sam")
    
    states = [] 
    states.append(StartMenu())

    while pygame_running(screen):
        dt = clock.tick(60) / 1000.0

        state = states[-1]

        state.game_loop(dt)
        state.draw(screen)

        if state.is_finished():
            states.pop()

        for next in state.next_state():
            states.append(next)        

        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()