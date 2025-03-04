import pygame


def init():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Arcade Game")
    clock = pygame.time.Clock()
    return screen, clock


def draw_line():
    screen, clock = init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((255, 255, 255))
        pygame.draw.aaline(screen, (0, 0, 0), (0, 0), (600, 600))
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    draw_line()
