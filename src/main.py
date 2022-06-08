import constants
import pygame
from game_states import StartMenu

from level import resource_path

def pygame_running(screen) -> bool:

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
    pygame.display.set_icon(pygame.image.load(resource_path("./resources/icon.icns")))
    pygame.display.set_caption("Nano-Golf - Ayan & Sam")
    
    states = [] 
    states.append(StartMenu())
    
    constants.FONT_BIG = pygame.font.SysFont(None, 60, bold=True)
    constants.FONT_NORMAL = pygame.font.SysFont(None, 32)


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