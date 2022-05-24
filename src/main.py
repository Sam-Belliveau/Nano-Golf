import pygame

from level import Level

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

    screen = pygame.display.set_mode([500, 500])

    while game_loop(screen):
        world = pygame.Rect(0, 0, 500, 500)
        screen.blit(pygame.transform.scale(level.surface, (500, 500)), world)
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()