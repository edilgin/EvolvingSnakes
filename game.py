from Snake import Snake
from Genetics import GeneticAlgorithm
import pygame
import time

import numpy as np
import random
import pickle

class game_control:
    def __init__(self, col_row_size, space):
        self.board = []
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
        if snake.counter == 120:
            snake.game_over = True

        food_x = snake.food_pos[0]
        food_y = snake.food_pos[1]
        snake_x = snake.position[0][0]
        snake_y = snake.position[0][1]

        if  snake_x == food_x and  snake_y == food_y:
            snake.create_food()
            snake.add_node()
            snake.score += 20 * len(snake.position)
            snake.counter = 0

    def board_update(self, snake):
        self.board = [[0 for _ in range(11)] for _ in range(11)]

        for i in range(len(self.board[0])):
            self.board[0][i] = -2
            self.board[-1][i] = -2
            self.board[i][0] = -2
            self.board[i][-1] = -2

        food_x = snake.food_pos[0] // self.node_size
        food_y = snake.food_pos[1] // self.node_size

        snake_head_x = snake.position[0][0] // self.node_size
        snake_head_y = snake.position[0][1] // self.node_size
        self.board[food_y-1][food_x-1] = 1
        self.board[snake_head_y-1][snake_head_x-1] = -1

        for node in snake.position[1:]:
            x,y = node[0] // self.col_row_size, node[1] // self.col_row_size
            self.board[y-1][x-1] = -1
        return self.board

    def vision(self, snake):
        vision_snake = np.array([0 for _ in range(20)])

        head_x, head_y = snake.position[0][0], snake.position[0][1]
        food_x, food_y = snake.food_pos[0], snake.food_pos[1]
        tail_x, tail_y = snake.position[-1][0], snake.position[-1][0]

        if head_x - food_x == 0:
            if head_y > food_y:                         # if the food is above the snake
                vision_snake[0] = head_y - food_y
            else:                                       # if the food is below the snake
                vision_snake[1] = food_y - head_y

        if head_y - food_y == 0:
            if head_x > food_x:                         # if the food is left to the snake
                vision_snake[2] = head_x - food_x
            else:                         # if the food is right to the snake
                vision_snake[3] = food_x - head_x

        if head_x - food_x == head_y - food_y:       # if the food is diagonal to the snake
            if head_x - food_x > 0:
                if head_y - food_y > 0:
                    vision_snake[4] = ((head_x - food_x)**2 + (head_y - food_y)**2)**(1/2)
                else:
                    vision_snake[5] = ((head_x - food_x)**2 + (head_y - food_y)**2)**(1/2)
            else:
                if head_y - food_y > 0:
                    vision_snake[6] = ((head_x - food_x)**2 + (head_y - food_y)**2)**(1/2)
                else:
                    vision_snake[7] = ((head_x - food_x)**2 + (head_y - food_y)**2)**(1/2)

        if head_x - tail_x == 0:
            if head_y > tail_y:                             # if the tail is above the snake
                vision_snake[8] = head_y - tail_y
            else:                                           # if the tail is below the snake
                vision_snake[9] = tail_y - head_y
        if head_y - tail_y == 0:
            if head_x > tail_x:                             # if the tail is left to the snake
                vision_snake[10] = head_x - tail_x
            else:                                           # if the tail is right to the snake
                vision_snake[11] = tail_x - head_x

        if head_x - tail_x == head_y - tail_y:              # if the tail is diagonal to the snake
            if head_x - tail_x > 0:
                if head_y - tail_y > 0:
                    vision_snake[12] = ((head_x - tail_x) ** 2 + (head_y - tail_y) ** 2) ** (1 / 2)
                else:
                    vision_snake[13] = ((head_x - tail_x) ** 2 + (head_y - tail_y) ** 2) ** (1 / 2)
            else:
                if head_y - food_y > 0:
                    vision_snake[14] = ((head_x - tail_x) ** 2 + (head_y - tail_y) ** 2) ** (1 / 2)
                else:
                    vision_snake[15] = ((head_x - tail_x) ** 2 + (head_y - tail_y) ** 2) ** (1 / 2)

        vision_snake[16] = head_x
        vision_snake[17] = 9 - head_x
        vision_snake[18] = head_y
        vision_snake[19] = 9 - head_y

        vision_snake = vision_snake / 10

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
        if snake.counter > 100:
            snake.game_over = True

def create_controllers(gen_size):
    controller_list = []
    for j in range(gen_size):
        controller_list.append(game_control(col_row_size, spaces))
    return controller_list

col_row_size=30
spaces=10
node_size = col_row_size + spaces

snakes = []
prev_gen_snakes = []

SCREEN_WIDTH = 390
SCREEN_HEIGHT = 390

pop_size = 1000

controllers = create_controllers(pop_size)
gen = 0
ga = GeneticAlgorithm()
snakes = ga.initiate_population(snakes, pop_size)
dead_snakes = []
fittest_snakes_each_gen = []
generation_length = 40
max_score = 0

for generation in range(generation_length):
    max_score = 0
    while len(snakes) != 0:
        fittest_snakes_each_gen.append(snakes[0])
        for snake, controller in zip(snakes, controllers):
            snake.move()
            controller.check_snake(snake)
            inputs = controller.vision(snake)
            snake.predict(inputs)
            controller.check_death(snake)
            snake.score += 1
            snake.counter += 1

            if snake.score > fittest_snakes_each_gen[generation].score:
                fittest_snakes_each_gen[generation] = snake
                max_score = snake.score
            if snake.game_over:
                snakes.remove(snake)
                dead_snakes.append(snake)
                controllers.remove(controller)
    else:
        controllers = create_controllers(pop_size)
        snakes = ga.roulette_wheel(dead_snakes)
        dead_snakes.clear()
        gen += 1
        print("gen: {} max:{}".format(gen, max_score))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # set screen size
clock = pygame.time.Clock()                                         # clock will be used for determining frames per second

for generation in range(generation_length):
    current_snake = fittest_snakes_each_gen[generation]
    current_snake.reset()
    controller = game_control(col_row_size, spaces)
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
