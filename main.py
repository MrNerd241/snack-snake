import pygame
import random
from typing import Final

pygame.init()

difficulty = 'normal'

WIDTH: Final = 1295
HEIGHT: Final = 650
BLOCK_SIZE: Final = 20
FOOD_SIZE: Final = BLOCK_SIZE * 2
SNAKE_COLOR: Final = (0, 255, 0)
BACKGROUND_COLOR: Final = (0, 0, 0)
BUTTON_COLOR: Final = (0, 0, 255)
BUTTON_HOVER_COLOR: Final = (0, 100, 255)
TEXT_COLOR: Final = (255, 255, 255)

if difficulty == 'normal':
    FPS = 15
elif difficulty == 'easy':
    FPS = 10
elif difficulty == 'hard':
    FPS = 20
else:
    FPS = 15

fullscreen = False
original_size = (WIDTH, HEIGHT)
high_score = 0

def draw_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(window, SNAKE_COLOR, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))

def display_message(message, color, font_size, x, y):
    font = pygame.font.SysFont("consolas", font_size)
    text_surface = font.render(message, True, color)
    window.blit(text_surface, [x, y])

def draw_button(text, x, y, width, height, color, hover_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)
    
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(window, hover_color, button_rect)
        if mouse_click[0]:
            return True
    else:
        pygame.draw.rect(window, color, button_rect)
    
    display_message(text, TEXT_COLOR, 30, x + 10, y + 10)
    return False

def start_screen():
    global fullscreen, window
    while True:
        window.fill(BACKGROUND_COLOR)
        display_message("Snack Snake", (255, 255, 0), 60, WIDTH // 4, HEIGHT // 4 - 100)
        
        if draw_button("Start", WIDTH // 3, HEIGHT // 2 - 30, 200, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR):
            fullscreen = True
            window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            break

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def game_over_screen(score):
    global high_score
    if score > high_score:
        high_score = score
        with open('high_score.txt', 'w') as f:
            f.write(str(high_score))

    while True:
        window.fill(BACKGROUND_COLOR)
        display_message(f"Game Over! Score: {score}", (255, 0, 0), 50, WIDTH // 4, HEIGHT // 2 - 80)
        display_message(f"High Score: {high_score}", (0, 255, 255), 40, WIDTH // 4, HEIGHT // 2)
        
        if draw_button("Restart", WIDTH // 3, HEIGHT // 2 + 80, 200, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR):
            return True
        if draw_button("Quit", WIDTH // 3, HEIGHT // 2 + 160, 200, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR):
            return False

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def main():
    global window, fullscreen, high_score, FOOD_COLOR
    clock = pygame.time.Clock()
    window = pygame.display.set_mode(original_size)
    pygame.display.set_caption("Snack Snake")
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    try:
        with open('high_score.txt', 'r') as f:
            high_score = int(f.read())
    except FileNotFoundError:
        high_score = 0

    while True:
        start_screen()
        snake_list = []
        snake_length = 1
        snake_x = WIDTH // 2
        snake_y = HEIGHT // 2
        snake_speed_x = 0
        snake_speed_y = 0

        food_x = round(random.randrange(0, WIDTH - FOOD_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(0, HEIGHT - FOOD_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        FOOD_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        score = 0

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_a) and snake_speed_x == 0:
                        snake_speed_x = -BLOCK_SIZE
                        snake_speed_y = 0
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and snake_speed_x == 0:
                        snake_speed_x = BLOCK_SIZE
                        snake_speed_y = 0
                    elif event.key in (pygame.K_UP, pygame.K_w) and snake_speed_y == 0:
                        snake_speed_y = -BLOCK_SIZE
                        snake_speed_x = 0
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and snake_speed_y == 0:
                        snake_speed_y = BLOCK_SIZE
                        snake_speed_x = 0
                    elif event.key == pygame.K_p:
                        paused = not paused
                    elif event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            window = pygame.display.set_mode(original_size)

            if paused:
                continue

            snake_x += snake_speed_x
            snake_y += snake_speed_y

            if snake_x >= WIDTH or snake_x < 0 or snake_y >= HEIGHT or snake_y < 0:
                running = False

            snake_head = [snake_x, snake_y]
            snake_list.append(snake_head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            if snake_x in range(food_x, food_x + FOOD_SIZE) and snake_y in range(food_y, food_y + FOOD_SIZE):
                food_x = round(random.randrange(0, WIDTH - FOOD_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                food_y = round(random.randrange(0, HEIGHT - FOOD_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                FOOD_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                snake_length += 1
                score += 5
                if score == 100:
                    score *= 2

            for segment in snake_list[:-1]:
                if segment == snake_head:
                    running = False
                    break

            window.fill(BACKGROUND_COLOR)
            draw_snake(snake_list)
            pygame.draw.rect(window, FOOD_COLOR, pygame.Rect(food_x, food_y, FOOD_SIZE, FOOD_SIZE))
            display_message(f"Score: {score}", (255, 255, 255), 20, 10, 10)

            pygame.display.flip()
            clock.tick(FPS)

        if not game_over_screen(score):
            break

    pygame.quit()

if __name__ == "__main__":
    main()
