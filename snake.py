import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import random
import sys

# ----------------------------
# Konstanten
# ----------------------------
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 7 # Grundgeschwindigkeit

# Farben
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)

# Highscore-Datei
HIGHSCORE_FILE = "highscore.txt"

# ----------------------------
# Pygame Initialisierung
# ----------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# ----------------------------
# Hilfsfunktionen
# ----------------------------
def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_highscore(score):
    highscore = load_highscore()
    if score > highscore:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))

# ----------------------------
# Snake Klasse
# ----------------------------
class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL_SIZE, 0)
        self.grow_flag = False

    def move(self):
        new_head = (self.body[0][0] + self.direction[0],
                    self.body[0][1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def collision(self):
        head = self.body[0]
        return (head[0] < 0 or head[0] >= WIDTH or
                head[1] < 0 or head[1] >= HEIGHT or
                head in self.body[1:])

# ----------------------------
# Food Klasse
# ----------------------------
class Food:
    def __init__(self):
        self.position = self.random_pos()

    def random_pos(self):
        return (random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE)

# ----------------------------
# Game Funktionen
# ----------------------------
def game_loop():
    snake = Snake()
    food = Food()
    score = 0

    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, CELL_SIZE):
                    snake.direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -CELL_SIZE):
                    snake.direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and snake.direction != (CELL_SIZE, 0):
                    snake.direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-CELL_SIZE, 0):
                    snake.direction = (CELL_SIZE, 0)

        # Snake bewegen
        snake.move()

        # Essen prüfen
        if snake.body[0] == food.position:
            score += 1
            snake.grow()
            food.position = food.random_pos()

        # Kollision prüfen
        if snake.collision():
            save_highscore(score)
            return score

        # Bildschirm zeichnen
        screen.fill(BLACK)
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (food.position[0], food.position[1], CELL_SIZE, CELL_SIZE))
        draw_text(f"Score: {score}", WHITE, 10, 10)
        draw_text(f"Highscore: {load_highscore()}", BLUE, 10, 40)

        pygame.display.flip()
        clock.tick(FPS)

def start_screen():
    screen.fill(BLACK)
    draw_text("SNAKE GAME", GREEN, WIDTH//2 - 100, HEIGHT//2 - 60)
    draw_text("Press ENTER to start", WHITE, WIDTH//2 - 130, HEIGHT//2)
    draw_text("Press ESC to quit", WHITE, WIDTH//2 - 110, HEIGHT//2 + 40)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_over_screen(score):
    screen.fill(BLACK)
    draw_text("GAME OVER", RED, WIDTH // 2 - 80, HEIGHT // 2 - 60)
    draw_text(f"Score: {score}", WHITE, WIDTH // 2 - 50, HEIGHT // 2 - 20)
    draw_text(f"Highscore: {load_highscore()}", BLUE, WIDTH // 2 - 70, HEIGHT // 2 + 20)
    draw_text("Press ENTER to restart or ESC to quit", WHITE, WIDTH // 2 - 180, HEIGHT // 2 + 60)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# ----------------------------
# Hauptschleife
# ----------------------------
while True:
    start_screen()
    final_score = game_loop()
    restart = game_over_screen(final_score)
    if not restart:
        break
