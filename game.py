from SnakeGame import Snake
from Genetics import GeneticAlgorithm
import numpy as np
import pygame

class game_control:
    def __init__(self, game_cols, game_rows, col_row_size, space, x_pos_board, y_pos_board):
        self.board = []
        self.columns = game_cols
        self.rows = game_rows
        self.col_row_size = col_row_size
        self.space = space
        self.node_size = self.col_row_size + self.space     # node size is space and the row size combined

        self.x_pos_board = x_pos_board
        self.y_pos_board = y_pos_board

        self.snake_start_x = (self.columns // 2) * self.node_size
        self.snake_start_y = (self.rows // 2 ) * self.node_size

    def draw(self, snake):
        food_x = snake.food_pos[0] + self.x_pos_board
        food_y = snake.food_pos[1] + self.y_pos_board

        pygame.draw.rect(screen, "red", (food_x, food_y, self.col_row_size, self.col_row_size))
        grid_width = (self.node_size * self.columns) - self.space
        grid_height = (self.node_size * self.rows) - self.space
        headx, heady = snake.position[0][0], snake.position[0][1]

        if 0 < headx < grid_width:
            if 0 < heady < grid_height:
                pygame.draw.rect(screen, "green", (headx + self.x_pos_board, heady+ self.y_pos_board, self.col_row_size, self.col_row_size))
        for node in snake.position[1:]:
            node_x = node[0] + self.x_pos_board
            node_y = node[1] + self.y_pos_board
            pygame.draw.rect(screen, "green", (node_x, node_y, self.col_row_size, self.col_row_size))


    def check_snake(self, snake):
        snake_rect = pygame.Rect(snake.position[0][0], snake.position[0][1], self.col_row_size, self.col_row_size)
        food_rect = pygame.Rect(snake.food_pos[0], snake.food_pos[1], self.col_row_size, self.col_row_size)

        if snake.counter == 120:
            snake.game_over = True
        if snake_rect.colliderect(food_rect):
            snake.create_food()
            snake.add_node()
            snake.score += 40
            snake.counter = 0

    def board_update(self, snake):
        self.board = [[0 for _ in range(self.columns+1)] for _ in range(self.rows+1)]

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
        vision_snake = [0 for _ in range(20)]

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
        vision_snake[17] = ((self.columns * self.node_size) - self.space) - head_x
        vision_snake[18] = head_y
        vision_snake[19] = ((self.rows * self.node_size) - self.space) - head_y


        return vision_snake

    def check_death(self, snake):
        # check if player hit a wall
        grid_width = (self.node_size * self.columns) - self.space
        grid_height = (self.node_size * self.rows) - self.space

        if 0 > snake.position[0][0] or grid_width < snake.position[0][0]:
            snake.game_over = True
        if 0 > snake.position[0][1] or grid_height < snake.position[0][1]:
            snake.game_over = True

        # check if the player hit itself
        snake_head = pygame.Rect(snake.position[0][0], snake.position[0][1], self.col_row_size, self.col_row_size)
        for node in snake.position[1:]:
            node = pygame.Rect(node[0], node[1], self.col_row_size, self.col_row_size)
            if snake_head.colliderect(node):
                snake.game_over = True
        snake.counter += 1
        if snake.counter > 100:
            snake.game_over = True


def draw_grids(grids_x, grids_y, cols, rows, size, spaces):
    x = ((size + spaces) * cols) - spaces
    y = ((size + spaces) * rows) - spaces
    x_pos_board = 0
    y_pos_board = 0
    for i in range(grids_x):                # 10
        for j in range(grids_y):            # 6
            pygame.draw.rect(screen, "grey", (x_pos_board, y_pos_board, x, y), width=2)
            x_pos_board = x * i
            y_pos_board = y * j
    pygame.draw.rect(screen, "grey", (x_pos_board, y_pos_board, x, y), width=2)


cols=10
rows=10
col_row_size=10
spaces=2
node_size = col_row_size + spaces


snakes = []
prev_gen_snakes = []

SCREEN_WIDTH = 1420
SCREEN_HEIGHT = 710

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # set screen size
clock = pygame.time.Clock()                     # clock will be used for determining frames per second

pop_size = 1000

screen_x = (node_size * cols) - spaces
screen_y = (node_size *rows) - spaces

def create_controllers():
    controller_list = []
    x, y = 0, 0
    for j in range(10):
        for i in range(100):
            controller_list.append(game_control(cols,rows, col_row_size, spaces,x, y))
            x = ((cols * node_size) - spaces) * i
            y = ((rows * node_size) - spaces) * j
    return controller_list

controllers = create_controllers()
gen = 0
max_score = 0
ga = GeneticAlgorithm(cols, rows, node_size, controllers[0].snake_start_x, controllers[0].snake_start_y)
snakes = ga.initiate_population(snakes, pop_size)
dead_snakes = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("black")
    draw_grids(12,6,10,10,10,2)

    if len(snakes) != 0:
        max_score = 0

        for snake, controller in zip(snakes, controllers):
            snake.move()
            controller.draw(snake)
            controller.check_snake(snake)
            inputs = controller.vision(snake)
            snake.predict(inputs)
            controller.check_death(snake)
            snake.score += 1
            snake.counter += 1

            if snake.score > max_score:
                max_score = snake.score
            if snake.game_over:
                snakes.remove(snake)
                snake.reset()
                dead_snakes.append(snake)
                controllers.remove(controller)
    else:
        controllers = create_controllers()
        snakes = ga.choose_snakes(dead_snakes)
        dead_snakes.clear()
        gen +=1
        print("gen: {} max:{}".format(gen,max_score))

    pygame.display.update()
    clock.tick(100)
