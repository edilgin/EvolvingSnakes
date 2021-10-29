from NeuralNetwork import NeuralNetwork
import random
import numpy as np

class Snake:
    def __init__(self, rows, cols, weights, node_size, x, y):
        self.columns = cols                            # how many columns are on the board
        self.rows = rows                               # how many rows are on the board

        self.node_size = node_size     # node size is space and the row size combined
        self.counter = 0
        self.score = 1
        self.fitness = 0
        self.game_over = False
        self.direction = "up"
        self.x, self.y = x, y
        self.position = [[x,y]]
        self.food_pos = [random.randint(0, self.columns-1) * self.node_size, random.randint(0, self.rows-1) * self.node_size]
        self.weights = weights
        # create the brain for the snake and initialize it
        self.brain = NeuralNetwork([20,15,15,4])

        if len(self.weights) == 0:
            self.brain.initializeNetwork()
        else:
            self.brain.parameters = weights

    def move(self):
        prev_location = [self.position[0][0], self.position[0][1]]      # x and y of the snakes head is used as first prev_location
        for i in range(len(self.position)):
            new_prev_location = [self.position[i][0], self.position[i][1]]
            self.position[i][0], self.position[i][1] = prev_location[0], prev_location[1]
            prev_location = new_prev_location

        # lastly move the head of the snake
        if self.direction == "up":
            self.position[0][1] -= self.node_size
        elif self.direction == "down":
            self.position[0][1] += self.node_size
        elif self.direction == "right":
            self.position[0][0] += self.node_size
        elif self.direction == "left":
            self.position[0][0] -= self.node_size

    def add_node(self):
        if self.direction == "up":
            self.position.append([self.position[-1][0], self.position[-1][1] + self.node_size])
        if self.direction == "down":
            self.position.append([self.position[-1][0], self.position[-1][1] - self.node_size])
        if self.direction == "right":
            self.position.append([self.position[-1][0] - self.node_size, self.position[-1][1]])
        if self.direction == "left":
            self.position.append([self.position[-1][0] + self.node_size, self.position[-1][1]])

    def predict(self, inputs):
        X = np.array(inputs).flatten()          # X = inputs
        prediction = self.brain.forwardProp(X)
        change = "up"
        if prediction == 0:
            change = "up"
        if prediction == 1:
            change = "down"
        if prediction == 2:
            change = "left"
        if prediction == 3:
            change = "right"

        if change == "up" and self.direction != "down":
            self.direction = "up"
        if change == "down"  and self.direction != "up":
            self.direction = "down"
        if change == "left" and self.direction != "right":
            self.direction = "left"
        if change == "right" and self.direction != "left":
            self.direction = "right"

    def reset(self):
        self.game_over = False
        self.direction = "up"
        self.score = 1
        self.fitness = 0
        self.counter = 0
        self.position = [[self.x, self.y]]
        self.food_pos = [random.randint(0, self.columns-1) * self.node_size, random.randint(0, self.rows-1) * self.node_size]

    def create_food(self):
        positionX = random.randint(0, self.columns - 1) * self.node_size
        positionY = random.randint(0, self.rows - 1) * self.node_size
        self.food_pos = [positionX, positionY]
