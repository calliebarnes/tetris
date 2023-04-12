import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetrominoes
TETROMINOES = [
    [
        [1, 1, 1],
        [1, 0, 0]
    ],
]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        # Draw the game board, tetrominoes, and other elements here
        pygame.display.flip()

if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()