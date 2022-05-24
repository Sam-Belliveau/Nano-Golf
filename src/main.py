import pygame

from level import Level

def game_loop(screen) -> bool:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    # Fill the background with white
    screen.fill((255, 255, 255))


    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)


    return True


def main():
    level = Level("./resources/L1.png")
    print(level)    
    print(level.sectors)

    pygame.init()

    screen = pygame.display.set_mode([500, 500])

    while game_loop(screen):
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()