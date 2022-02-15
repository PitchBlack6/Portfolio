# Attempted to feed the entire game screen into the network.
# Even with a small game board the AI takes too long to learn anything and repeatedly goes extinct.

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
bg_colour = 0x000000
snake_colour = 0xFFFFFF
head_colour = 0x00FFFF
food_colour = 0x00FF00

# Pixel size
pix = 10.0
game_speed = 100

# Screen size
disp_x = 20 * pix
disp_y = 20 * pix

# Initializing learning variables
best_foods = 0
best_fitness = 0
loop_punishment = 0.25
near_food_score = 0.2
moved_score = 0.01
gen_num = 0


def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj


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
    def snake_body(snake_list):
        for i in snake_list[0:-1]:
            pygame.draw.rect(dis, white, [i[0], i[1], pix, pix])
        head = snake_list[-1]
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
    dx = 0
    dy = -pix

    # Set food location at food
    food_x = round(random.randrange(0, disp_x - pix) / pix) * pix
    food_y = round(random.randrange(0, disp_y - pix) / pix) * pix

    # Set initial snake body
    snake_list = [[snake_x, snake_y], [snake_x, snake_y + pix], [snake_x, snake_y + pix]]
    snake_len = 3

    # Draw starting snake
    snake_body(snake_list)

    # Loops forever until window is closed
    while not game_over:
        time_alive += 1
        b += 1
        if b == 200:
            game_over = True

        pygame.event.get()
        # Put screen into matrix
        screen = pygame.surfarray.pixels2d(dis)
        screen_arr = get_screen(screen)
        output = net.activate(get_screen(screen))
        max_output = max(output)
        move = output.index(max_output)

        if move == 0:
            dx = -pix
            dy = 0
        if move == 1:
            dx = pix
            dy = 0
        if move == 2:
            dx = 0
            dy = -pix
        if move == 3:
            dx = 0
            dy = pix
        if move == 4:
            pass

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
    return (snake_len - 3) * 10 + time_alive - 30


# Turns the screen into a simplified matrix so the AI doesn't need to look at every pixel
def get_screen(scr):
    global bg_colour
    global snake_colour
    global head_colour
    global food_colour
    global pix
    scr_arr = []

    for i, x in enumerate(scr):
        if i % pix == 0:
            for j, y in enumerate(x):
                if j % pix == 0:
                    if scr[i][j] == bg_colour:
                        scr_arr.append(0)
                    elif scr[i][j] == snake_colour:
                        scr_arr.append(1)
                    elif scr[i][j] == head_colour:
                        scr_arr.append(2)
                    elif scr[i][j] == food_colour:
                        scr_arr.append(3)

    return scr_arr


def save_best(inst, filename='trained/best_generation.pickle'):
    instances = []
    if os.path.isfile(filename):
        inst = load_object(filename)
    instances.append(inst)
    save_object(instances, filename)


def run(path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         path)

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

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
