from Genetics import GeneticAlgorithm
import pygame
import time
import numpy as np

class game_control:                                                 # write a class for playing the game
    def __init__(self, col_row_size, space):
        self.col_row_size = col_row_size
        self.space = space
        self.node_size = self.col_row_size + self.space     # node size is space and the row size combined

    def draw(self, snake):
        food_x = snake.food_pos[0]
        food_y = snake.food_pos[1]
        headx = snake.position[0][0]
        heady = snake.position[0][1]

        food_x = food_x * self.node_size
        food_y = food_y * self.node_size
        pygame.draw.rect(screen, "red", (food_x, food_y, self.col_row_size, self.col_row_size))

        pygame.draw.rect(screen, "green", (headx * self.node_size, heady * self.node_size, self.col_row_size, self.col_row_size))
        for node in snake.position[1:]:
            node_x = node[0] * self.node_size
            node_y = node[1] * self.node_size
            pygame.draw.rect(screen, "green", (node_x, node_y, self.col_row_size, self.col_row_size))

    def check_snake(self, snake):
        food_x = snake.food_pos[0]
        food_y = snake.food_pos[1]
        snake_x = snake.position[0][0]
        snake_y = snake.position[0][1]

        if  snake_x == food_x and  snake_y == food_y:
            snake.create_food()
            snake.add_node()
            snake.score += 1
            snake.counter = 0

    def vision(self, snake):
        vision_snake = [0 for _ in range(24)]

        head_x, head_y = snake.position[0][0], snake.position[0][1]
        food_x, food_y = snake.food_pos[0], snake.food_pos[1]
        tail_x, tail_y = snake.position[-1][0], snake.position[-1][0]

        if head_x - food_x == 0:
            if head_y > food_y:                         # if the food is above the snake
                vision_snake[0] = 1
            else:                                       # if the food is below the snake
                vision_snake[1] = 1

        if head_y - food_y == 0:
            if head_x > food_x:                         # if the food is left to the snake
                vision_snake[2] = 1
            else:                         # if the food is right to the snake
                vision_snake[3] = 1

        if head_x - food_x == head_y - food_y:       # if the food is diagonal to the snake
            if head_x - food_x > 0:
                if head_y - food_y > 0:
                    vision_snake[4] = 1
                else:
                    vision_snake[5] = 1
            else:
                if head_y - food_y > 0:
                    vision_snake[6] = 1
                else:
                    vision_snake[7] = 1

        if head_x - tail_x == 0:
            if head_y > tail_y:                             # if the tail is above the snake
                vision_snake[8] = 1
            else:                                           # if the tail is below the snake
                vision_snake[9] = 1
        if head_y - tail_y == 0:
            if head_x > tail_x:                             # if the tail is left to the snake
                vision_snake[10] = 1
            else:                                           # if the tail is right to the snake
                vision_snake[11] = 1

        if head_x - tail_x == head_y - tail_y:              # if the tail is diagonal to the snake
            if head_x - tail_x > 0:
                if head_y - tail_y > 0:
                    vision_snake[12] = 1
                else:
                    vision_snake[13] = 1
            else:
                if head_y - food_y > 0:
                    vision_snake[14] = 1
                else:
                    vision_snake[15] = 1

        vision_snake[16] = head_x / 10
        vision_snake[17] = (9 - head_x) / 10
        vision_snake[18] = head_y / 10
        vision_snake[19] = (9 - head_y) / 10
        vision_snake[20] = ((head_x**2 + head_y**2)**(1/2)) / 10
        vision_snake[21] = ((head_x**2 + (9-head_y)**2)**(1/2)) / 10
        vision_snake[22] = (((9-head_x)**2 + head_y**2)**(1/2)) / 10
        vision_snake[23] = (((9-head_x)**2 + (9-head_y)**2)**(1/2)) / 10

        return vision_snake

    def check_death(self, snake):
        # check if player hit a wall
        snake_x = snake.position[0][0]
        snake_y = snake.position[0][1]
        if 0 > snake_x or 9 < snake_x:
            snake.game_over = True
        if 0 > snake_y or 9 < snake_y:
            snake.game_over = True

        # check if the player hit itself
        for node in snake.position[1:]:
            if snake_x == node[0] and snake_y == node[1]:
                snake.game_over = True
        snake.counter += 1

        if snake.counter > 200:
            snake.game_over = True

col_row_size=30
spaces=10
node_size = col_row_size + spaces

snakes = []
prev_gen_snakes = []

SCREEN_WIDTH = 390
SCREEN_HEIGHT = 390

pop_size = 3000

controller = game_control(col_row_size, spaces)
gen = 0
ga = GeneticAlgorithm()

snakes = ga.initiate_population(snakes, pop_size)
dead_snakes = []
fittest_snakes_each_gen = []
generation_length = 50
max_score = 0

for generation in range(generation_length):                         # how many times the game will run
    max_score = 0                                                   # for each generation max_score is initialized as zero
    while len(snakes) != 0:                                         # while snakes list is not empty in other words as long as a snake is alive continue playing
        fittest_snakes_each_gen.append(snakes[0])                   # a random snake is added to the list but later if a fitter snake is found they are replaced with this random snake
        for snake in snakes:                                        # make every individual snake play the game
            snake.move()
            controller.check_snake(snake)
            inputs = controller.vision(snake)
            snake.predict(inputs)
            controller.check_death(snake)
            snake.counter += 1                                      # every frame snakes counter increases by one if reaches a threshold snake dies
                                                                    # to reset the counter snake must eat

            if snake.game_over:

                if snake.score > fittest_snakes_each_gen[generation].score:             # if current snake is better than the most fit previous snake
                    fittest_snakes_each_gen[generation] = snake     # most fit snake is set as the current snake
                    max_score = snake.score                         # max score of the generation is set as the current snakes score

                snakes.remove(snake)                                # if snake is dead remove it from playing snakes list
                dead_snakes.append(snake)                           # add it to the dead snakes list
    print("gen: {} max:{}".format(gen, max_score))
    snakes = ga.best_selection(dead_snakes)                         # when all the snakes die perform a roulette wheel selection with the dead snakes
    dead_snakes.clear()                                             # when our job ends with dead snakes we have to clean the list otherwise it will have snakes from other generations
    gen += 1

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # set screen size

for generation in range(generation_length):
    current_snake = fittest_snakes_each_gen[generation]
    current_snake.reset()
    while not current_snake.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill("black")
        current_snake.move()
        controller.draw(current_snake)
        controller.check_snake(current_snake)
        inputs = controller.vision(current_snake)
        current_snake.predict(inputs)
        controller.check_death(current_snake)
        current_snake.counter += 1
        pygame.display.update()
        time.sleep(0.06)
