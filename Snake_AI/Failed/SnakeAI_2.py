# Attempted to improve performance by changing the inputs and reducing the overall number of inputs

import random
import multiprocessing
import neat
import pygame
import os
import pickle

# Defining constants for game

# Colours (with a u)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 255, 255)
snake_colour = 0xFFFFFF

# Pixel size
pix = 10.0
game_speed = 50

# Screen size
disp_x = 30 * pix
disp_y = 30 * pix


# Main runtime function
def snake_main(genomes, config):
    # Create window
    pygame.init()
    dis = pygame.display.set_mode((disp_x, disp_y))
    pygame.display.set_caption('Snaaaake')
    pygame.display.update()

    # Initiate clock
    clock = pygame.time.Clock()

    # Draws body
    def snake_body(snk_lst):
        for j in snk_lst[0:-1]:
            pygame.draw.rect(dis, white, [j[0], j[1], pix, pix])
        head = snk_lst[-1]
        pygame.draw.rect(dis, blue, [head[0], head[1], pix, pix])

    # Initialize AI
    net = neat.nn.FeedForwardNetwork.create(genomes, config)

    # Initialize variables

    # Track game states
    game_over = False
    b = 0
    time_alive = 0

    # Set starting position
    snake_x = disp_x / 2
    snake_y = disp_y / 2
    pos = (snake_x, snake_y, pix, pix)

    # Set initial movement to 0
    dx = pix
    dy = 0

    # Set food location at food
    food_x = round(random.randrange(0, disp_x - pix) / pix) * pix
    food_y = round(random.randrange(0, disp_y - pix) / pix) * pix

    # Set initial snake body
    snake_list = [[snake_x, snake_y], [snake_x, snake_y + pix], [snake_x, snake_y + 2 * pix],
                  [snake_x, snake_y + 3 * pix], [snake_x, snake_y + 3 * pix]]
    snake_len = 3

    # snake_list = [[snake_x, snake_y]]
    # snake_len = 1

    # Draw starting snake
    snake_body(snake_list)

    # Loops forever until window is closed
    while not game_over:
        time_alive += 1

        b += 1
        if b > 25 * snake_len:
            game_over = True

        pygame.event.get()
        # Put screen into matrix
        screen = pygame.surfarray.pixels2d(dis)
        snake_inputs = get_screen(screen)
        snake_inputs.append(snake_x)
        snake_inputs.append(snake_y)
        snake_inputs.append(food_x)
        snake_inputs.append(food_y)
        output = net.activate(snake_inputs)
        move = output.index(max(output))

        if move == 0:
            pass
        elif move == 1:
            if dx == 0:
                dx = dy
                dy = 0
            elif dy == 0:
                dy = -dx
                dx = 0
        elif move == 2:
            if dx == 0:
                dx = -dy
                dy = 0
            elif dy == 0:
                dy = dx
                dx = 0

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
            b = 0
            a = True
            while a:
                a = False
                food_x = round(random.randrange(0, disp_x - pix) / pix) * pix
                food_y = round(random.randrange(0, disp_y - pix) / pix) * pix
                for i in snake_list:
                    if i == [food_x, food_y]:
                        a = True

        clock.tick(game_speed)

    pygame.quit()

    if time_alive <= 15:
        return 0
    return time_alive


# Turns the screen into a simplified matrix so the AI doesn't need to look at every pixel
def get_screen(scr):
    global snake_colour
    global pix
    scr_arr = []

    for i, x in enumerate(scr):
        if i % pix == 0:
            for j, y in enumerate(x):
                if j % pix == 0:
                    if scr[j][i] == snake_colour:
                        scr_arr.append(1.0)
                    else:
                        scr_arr.append(0.0)

    return scr_arr


def run(path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         path)

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(50, None))

    gen = neat.ParallelEvaluator(multiprocessing.cpu_count(), snake_main)
    winner = pop.run(gen.evaluate)
    print('\nBest genome:\n{!s}'.format(winner))

    with open('winner.pkl', 'wb')  as f:
        pickle.dump(winner, f)
        f.close()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "snake_config")
    run(config_path)
