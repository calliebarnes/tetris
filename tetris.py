import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRAVITY_DELAY = 1000
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_OFFSET_X = (SCREEN_WIDTH - GRID_SIZE * BOARD_WIDTH) // 2
BOARD_OFFSET_Y = (SCREEN_HEIGHT - GRID_SIZE * BOARD_HEIGHT) // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
AQUA = (0, 255, 255)
PURPLE = (128, 0, 128)

# Tetrominoes
TETROMINOES = [
    {"shape": [[1, 1, 1, 1]], "color": AQUA},  # I
    {"shape": [[1, 1], [1, 1]], "color": YELLOW},  # O
    {"shape": [[0, 1, 0], [1, 1, 1]], "color": PURPLE},  # T
    {"shape": [[0, 1, 1], [1, 1, 0]], "color": GREEN},  # S
    {"shape": [[1, 1, 0], [0, 1, 1]], "color": RED},  # Z
    {"shape": [[1, 0, 0], [1, 1, 1]], "color": BLUE},  # J
    {"shape": [[0, 0, 1], [1, 1, 1]], "color": ORANGE},  # L
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
        self.current_piece = Tetromino(
            5, 0, tetromino_data['shape'], tetromino_data['color'])
        self.gravity_timer = pygame.time.get_ticks()
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.next_piece = self.generate_random_tetromino()
        self.high_scores = self.load_high_scores()

    def darken_color(self, color, amount=30):
        r, g, b = color
        return max(0, r - amount), max(0, g - amount), max(0, b - amount)

    def run(self):
        while True:
            self.handle_events()
            if not self.paused and not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(30)

    def toggle_pause(self):
        self.paused = not self.paused

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause the game when the P key is pressed
                    self.toggle_pause()
                elif not self.paused:  # Only handle piece movement if the game is not paused
                    self.handle_piece_movement(event)
            
    def handle_piece_movement(self, event):
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
    
    def check_game_over(self):
        for x, cell in enumerate(self.board[0]):
            if cell:
                self.update_high_scores()
                self.game_over = True
                break

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.gravity_timer >= GRAVITY_DELAY // self.level:
            if not self.collision(0, 1):
                self.current_piece.move(0, 1)
            else:
                self.lock_tetromino()
                self.clear_lines()
                self.check_game_over()
            self.gravity_timer = current_time

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", 1, WHITE)
        self.screen.blit(text, (10, 10))

    def draw_lines_cleared(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Lines: {self.lines_cleared}", 1, WHITE)
        self.screen.blit(text, (10, 50))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_board()
        self.draw_tetromino(self.current_piece)
        self.draw_score()
        self.draw_lines_cleared()
        self.draw_next_piece()
        self.draw_level()
        if self.paused:
            self.draw_paused()
        if self.game_over:
            self.draw_game_over()
        pygame.display.flip()

    def draw_board(self):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen, cell, (BOARD_OFFSET_X + x * GRID_SIZE, BOARD_OFFSET_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                    pygame.draw.rect(
                        self.screen, WHITE, (BOARD_OFFSET_X + x * GRID_SIZE, BOARD_OFFSET_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        board_outline_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, 10 * GRID_SIZE, 20 * GRID_SIZE)
        pygame.draw.rect(self.screen, WHITE, board_outline_rect, 3)
  
    def draw_tetromino(self, tetromino):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, tetromino.color, (BOARD_OFFSET_X + (tetromino.x + x) * GRID_SIZE, BOARD_OFFSET_Y + (tetromino.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                    pygame.draw.rect(self.screen, self.darken_color(tetromino.color), (BOARD_OFFSET_X + (tetromino.x + x) * GRID_SIZE, BOARD_OFFSET_Y + (tetromino.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def draw_paused(self):
        font = pygame.font.Font(None, 72)
        paused_text = font.render("Paused", True, WHITE)
        paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(paused_text, paused_rect)
    
    def draw_game_over(self):
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.draw_high_scores()

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

    def lock_tetromino(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece.x + x
                    board_y = self.current_piece.y + y

                    if board_y < 0:
                        self.game_over = True
                        return

                    self.board[board_y][board_x] = self.current_piece.color

        tetromino_data = random.choice(TETROMINOES)
        self.current_piece = Tetromino(
            5, 0, tetromino_data['shape'], tetromino_data['color'])
        self.current_piece = self.next_piece
        self.next_piece = self.generate_random_tetromino()

    def clear_lines(self):
        lines_to_clear = []

        for y, row in enumerate(self.board):
            if all(cell != 0 for cell in row):
                lines_to_clear.append(y)

        for line in lines_to_clear:
            del self.board[line]
            self.board.insert(0, [0] * 10)

        self.score += len(lines_to_clear) ** 2
        self.lines_cleared += len(lines_to_clear)

        if len(lines_to_clear) == 4:
            self.flash_animation(lines_to_clear)

        self.update_level()
    def generate_random_tetromino(self):
        tetromino_data = random.choice(TETROMINOES)
        return Tetromino(5, 0, tetromino_data['shape'], tetromino_data['color'])

    def draw_next_piece(self):
        next_piece_x, next_piece_y = 20, 2
        font = pygame.font.Font(None, 36)
        text = font.render("Next Piece:", 1, WHITE)
        self.screen.blit(text, (next_piece_x * GRID_SIZE, next_piece_y * GRID_SIZE))

        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.next_piece.color, ((next_piece_x + x) * GRID_SIZE, (next_piece_y + y + 2) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                    pygame.draw.rect(self.screen, WHITE, ((next_piece_x + x) * GRID_SIZE, (next_piece_y + y + 2) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def flash_animation(self, lines):
        for _ in range(2):  # Number of times to flash
            for line in lines:
                for x in range(BOARD_WIDTH):
                    pygame.draw.rect(
                        self.screen, WHITE,
                        (BOARD_OFFSET_X + x * GRID_SIZE, BOARD_OFFSET_Y + line * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0
                    )
            pygame.display.flip()
            pygame.time.delay(75)  # Time in milliseconds for the flash to stay on the screen

            self.draw_board()
            pygame.display.flip()
            pygame.time.delay(75)  # Time in milliseconds for the flash to stay off the screen

    def update_level(self):
        self.level = self.lines_cleared // 10 + 1
    
    def draw_level(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Level: {self.level}", 1, WHITE)
        self.screen.blit(text, (10, 90))

    def load_high_scores(self, file_name='high_scores.txt'):
        try:
            with open(file_name, 'r') as file:
                scores = [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            scores = [0] * 5  # Create a default list with 5 zeros if the file is not found
        return scores
    
    def save_high_scores(self, high_scores, file_name='high_scores.txt'):
        with open(file_name, 'w') as file:
            for score in high_scores:
                file.write(str(score) + '\n')

    def update_high_scores(self):
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]  # Keep only the top 5 scores
        self.save_high_scores(self.high_scores)

    def draw_high_scores(self):
        font = pygame.font.Font(None, 36)
        header = font.render("High Scores:", True, WHITE)
        self.screen.blit(header, (10, 130))

        for i, score in enumerate(self.high_scores, start=1):
            text = font.render(f"{i}. {score}", True, WHITE)
            self.screen.blit(text, (10, 130 + i * 40))


if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()
