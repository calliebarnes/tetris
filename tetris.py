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
    {"shape": [[1, 1, 1, 1]], "color": (0, 255, 255)},  # I
    {"shape": [[1, 1], [1, 1]], "color": (255, 255, 0)},  # O
    {"shape": [[0, 1, 0], [1, 1, 1]], "color": (128, 0, 128)},  # T
    {"shape": [[0, 1, 1], [1, 1, 0]], "color": (0, 255, 0)},  # S
    {"shape": [[1, 1, 0], [0, 1, 1]], "color": (255, 0, 0)},  # Z
    {"shape": [[1, 0, 0], [1, 1, 1]], "color": (0, 0, 255)},  # J
    {"shape": [[0, 0, 1], [1, 1, 1]], "color": (255, 165, 0)},  # L
]

class Tetromino:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def move(self, x, y):
        self.x += x
        self.y += y

    def rotate(self):
        self.shape = list(zip(*reversed(self.shape)))
        

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.board = [[0] * 10 for _ in range(20)]
        tetromino_data = random.choice(TETROMINOES)
        self.current_piece = Tetromino(5, 0, tetromino_data['shape'], tetromino_data['color'])

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotated_shape = list(zip(*reversed(self.current_piece.shape)))
                    if not self.collision(0, 0, rotated_shape):
                        self.current_piece.rotate()
                if event.key == pygame.K_DOWN:
                    if not self.collision(0, 1):
                        self.current_piece.move(0, 1)
                if event.key == pygame.K_LEFT:
                    if not self.collision(-1, 0):
                        self.current_piece.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if not self.collision(1, 0):
                        self.current_piece.move(1, 0)

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_board()
        self.draw_tetromino(self.current_piece)
        pygame.display.flip()

    def draw_board(self):
         for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)


    def draw_tetromino(self, tetromino):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, tetromino.color, ((tetromino.x + x) * GRID_SIZE, (tetromino.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                    pygame.draw.rect(self.screen, BLACK, ((tetromino.x + x) * GRID_SIZE, (tetromino.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def collision(self, x_move, y_move, rotated_shape=None):
        shape = rotated_shape if rotated_shape is not None else self.current_piece.shape
            
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece.x + x + x_move
                    board_y = self.current_piece.y + y + y_move

                        # Check for out-of-bounds conditions
                    if board_x < 0 or board_x >= len(self.board[0]) or board_y >= len(self.board):
                        return True

                        # Check for floor collision
                    if board_y < 0:
                        continue

                        # Check for collision with locked Tetrominos
                    if self.board[board_y][board_x]:
                        return True

        return False

if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()