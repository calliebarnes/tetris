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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Tetrominoes
I = [
    [1, 1, 1, 1]
]

J = [
    [1, 0, 0],
    [1, 1, 1]
]

L = [
    [0, 0, 1],
    [1, 1, 1]
]

O = [
    [1, 1],
    [1, 1]
]

S = [
    [0, 1, 1],
    [1, 1, 0]
]

T = [
    [0, 1, 0],
    [1, 1, 1]
]

Z = [
    [1, 1, 0],
    [0, 1, 1]
]
TETROMINOES = [I, J, L, O, S, T, Z]

# Board
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
def create_board():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


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
        self.board = create_board()
        self.draw_board()
        self.draw_tetromino(random.choice(TETROMINOES), 0, 0)
        pygame.display.flip()
    
    def draw_board(self):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x] == 0:
                    pygame.draw.rect(self.screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                else:
                    pygame.draw.rect(self.screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    def draw_tetromino(self, tetromino, x, y):
        for i in range(len(tetromino)):
            for j in range(len(tetromino[i])):
                if tetromino[i][j] == 1:
                    pygame.draw.rect(self.screen, WHITE, (x + j * GRID_SIZE, y + i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    def draw_text(self, text, x, y, color):
        font = pygame.font.SysFont('Arial', 30)
        text = font.render(text, True, color)
        self.screen.blit(text, (x, y))

if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()