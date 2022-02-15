import random
import time
import sys
import pygame

pygame.init()

# Defining constants

# Colours (with a u)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 255, 255)
yellow = (255, 255, 0)

# Pixel size
pix = 10

# Screen size
disp_x = 50 * pix
disp_y = 50 * pix

# Fonts
end_screen = pygame.font.SysFont("comicsansms", 20)
score_font = pygame.font.SysFont("comicsansms", 15)

# Create window
dis = pygame.display.set_mode((disp_x, disp_y))
pygame.display.set_caption('Snaaaake')
pygame.display.update()

# Initiate clock
clock = pygame.time.Clock()


# Define message position and colour
def message(msg, color):
    mesg = end_screen.render(msg, True, color)
    dis.blit(mesg, [disp_x / 3, disp_y / 3])


def snake_body(snake_list):
    for i in snake_list[0:-1]:
        pygame.draw.rect(dis, white, [i[0], i[1], pix, pix])
    head = snake_list[-1]
    pygame.draw.rect(dis, blue, [head[0], head[1], pix, pix])


def show_score(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


# Sets Difficulty
def set_diff():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 5
                if event.key == pygame.K_2:
                    return 10
                if event.key == pygame.K_3:
                    return 15
                if event.key == pygame.K_4:
                    return 30
                if event.key == pygame.K_5:
                    return 50


# Main runtime function
def snake_main():
    # initialize variables

    # Track game states
    game_over = False
    window_close = False

    # Set starting position
    snake_x = disp_x / 2
    snake_y = disp_y / 2
    pos = (snake_x, snake_y, pix, pix)

    # Set initial movement to 0
    dx = 0
    dy = -pix

    # Set food location at food
    food_x = round(random.randrange(0, disp_x - pix) / pix) * pix
    food_y = round(random.randrange(0, disp_y - pix) / pix) * pix

    # Set initial snake body
    snake_list = [[snake_x, snake_y], [snake_x , snake_y + pix]]
    snake_len = 2

    # Start Screen
    dis.fill(black)
    message("Welcome to Snake!", yellow)
    pygame.display.update()
    time.sleep(5)
    dis.fill(black)
    message("Select Difficulty: 1-5", yellow)
    pygame.display.update()
    game_speed = set_diff()
    # Draw starting snake
    snake_body(snake_list)

    # Loops forever until window is closed
    while not window_close:

        # Game Over Screen
        while game_over:

            # Clears screen and shows option to restart
            dis.fill(black)
            message("You lost! Score: " + str(snake_len - 1) + " Replay? Y/N", red)
            pygame.display.update()

            # Events Checker
            for event in pygame.event.get():
                # Checks if User pressed Y or N
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        snake_main()
                    if event.key == pygame.K_n:
                        game_over = False
                        window_close = True

                # Checks if User presses quit
                if event.type == pygame.QUIT:
                    game_over = False
                    window_close = True

        # Events Checke
        for event in pygame.event.get():
            # Checks for arrow keys or WASD or ESC
            if event.type == pygame.KEYDOWN:
                # If arrow keys or WASD is pressed, sets movement direction
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    dx = -pix
                    dy = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    dx = pix
                    dy = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    dx = 0
                    dy = -pix
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    dx = 0
                    dy = pix
                # If ESC is pressed, ends game
                elif event.key == pygame.K_ESCAPE:
                    game_over = True

            # Checks if User presses quit
            if event.type == pygame.QUIT:
                window_close = True

        # Snake head moves in current direction
        snake_x += dx
        snake_y += dy

        # Screen is reset
        dis.fill(black)

        # Food is drawn
        food = (food_x, food_y, pix, pix)
        pygame.draw.rect(dis, green, food)

        # Appends snake position to body
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)

        # Clears snake tail
        if len(snake_list) > snake_len:
            del snake_list[0]

        # Draws snake body
        snake_body(snake_list)

        # Displays Score
        show_score(snake_len - 1)

        # Lose conditions
        # If snake leaves boundaries
        if snake_x >= disp_x or snake_x < 0 or snake_y >= disp_y or snake_y < 0:
            game_over = True
        # If snake collides with itself
        for i in snake_list[:-1]:
            if i == snake_head:
                game_over = True

        # Refreshes screen
        pygame.display.update()

        # Checks if snake overlaps with food and respawns food.
        if snake_x == food_x and snake_y == food_y:
            snake_len += 1
            a = True
            while a:
                a = False
                food_x = round(random.randrange(0, disp_x - pix) / pix) * pix
                food_y = round(random.randrange(0, disp_y - pix) / pix) * pix
                for i in snake_list:
                    if i == [food_x, food_y]:
                        a = True

        # Waits for delay
        clock.tick(game_speed)

    # When game ends, displays closing message and closes window
    dis.fill(black)
    message("Thanks for playing!", red)
    pygame.display.update()
    time.sleep(2)

    pygame.quit()
    sys.exit()


# Runs main function
snake_main()
