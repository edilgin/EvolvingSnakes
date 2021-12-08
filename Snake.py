from NeuralNetwork import NeuralNetwork
import random
import numpy as np

class Snake:
    # weights parameter of the constructor is used for copying the snakes or creating a child from parent
    # for example if a snake has died we can take its brain and just create a new snake and pass the brain inside of the new snake
    # this is the same thing as copying the snakes. I implemented this kind of functionality because i couldnt find a good way
    # to copy classes. Other use case is creating a child from parents brain which also is something like copying
    def __init__(self, weights):
        # counter will be used to check how many moves snake makes. If too many moves are made snake will be killed
        self.counter = 0
        # score will be increased a lot whenever snake eats a food and a small amount every frame it survives
        self.score = 1
        # fitness will be calculated from score and it will be basically the probability that snake reproduces to create offspring
        self.fitness = 0
        self.game_over = False
        self.direction = "up"           # default direction is up
        self.position = [[5,5],[4,5]]         # default position of the snake is the middle
        self.food_pos = [random.randint(0, 9), random.randint(0, 9)]    # food is created randomly
        self.weights = weights

        # create the brain for the snake and initialize it
        self.brain = NeuralNetwork([24, 20, 4])

        # this is the part where we can use a dead snakes parameters on a newly instantiated snake
        if len(self.weights) == 0:                  # if no weights are passed then create a new brain
            self.brain.initializeNetwork()
        else:                                       # otherwise use the weight passed to the constructor
            self.brain.parameters = weights

    # this function moves the snake based on the direction it thinks it should move
    # all of the nodes of the snake moves to the position of the next node
    # and lastly the head of the snake is moved to where the direction of the snake points it
    def move(self):
        prev_location = [self.position[0][0], self.position[0][1]]      # x and y of the snakes head is used as first prev_location

        # loop for however many nodes are on the snake
        for i in range(len(self.position)):
            # self.position[i] is the current node we are working with
            new_prev_location = [self.position[i][0], self.position[i][1]]              # save the current nodes position
            # set the current nodes position to the next nodes position
            self.position[i][0], self.position[i][1] = prev_location[0], prev_location[1]
            prev_location = new_prev_location           # new prev location is set to the saved current nodes position

        # lastly move the head of the snake to the desired direction
        if self.direction == "up":
            self.position[0][1] -= 1
        elif self.direction == "down":
            self.position[0][1] += 1
        elif self.direction == "right":
            self.position[0][0] += 1
        elif self.direction == "left":
            self.position[0][0] -= 1

    # adds another node to the snake. It will be called every time a snake eats a food
    def add_node(self):
        # logic here is not hard to grasp so i will leave it uncommented
        if self.direction == "up":
            self.position.append([self.position[-1][0], self.position[-1][1] + 1])
        if self.direction == "down":
            self.position.append([self.position[-1][0], self.position[-1][1] - 1])
        if self.direction == "right":
            self.position.append([self.position[-1][0] - 1, self.position[-1][1]])
        if self.direction == "left":
            self.position.append([self.position[-1][0] + 1, self.position[-1][1]])

    # predict function returns what the neural network thinks it should do at a frame
    def predict(self, inputs):
        X = np.array(inputs).flatten()              # X = inputs
        prediction = self.brain.forwardProp(X)      # predictions are received after forward propagation through the network
        change = "up"

        # we turn neural networks outputs into the directions that snake should move
        if prediction == 0:
            change = "up"
        if prediction == 1:
            change = "down"
        if prediction == 2:
            change = "left"
        if prediction == 3:
            change = "right"

        # this part looks kind of redundant but i had to use it to prevent snakes from doing some random movements
        # still what we do is set the snakes direction based on the neural network of it
        if change == "up" and self.direction != "down":
            self.direction = "up"
        if change == "down"  and self.direction != "up":
            self.direction = "down"
        if change == "left" and self.direction != "right":
            self.direction = "left"
        if change == "right" and self.direction != "left":
            self.direction = "right"

    # we will use dead snakes in later generations so we must set their important properties such as
    # score, fitness, counter etc. to their initial value
    def reset(self):
        self.game_over = False                                          # basically turn dead snakes alive once again
        self.direction = "up"                                           # starting direction of the snake is always up
        self.score = 1                                                  # score, fitness, counter and position set to their initial value
        self.fitness = 0
        self.counter = 0
        self.position = [[5, 5], [4,5],[3,5]]
        self.food_pos = [random.randint(0, 9), random.randint(0, 9)]    # a random food pos is created

    # This function right now is missing because it places food randomly which may cause the food to spawn inside the snake and just add
    # +1 score
    def create_food(self):
        # there are 10 tiles vertically and horizontally
        positionX = random.randint(0, 9)                    # place the foods x pos between tiles 0-9
        positionY = random.randint(0, 9)                    # place the foods y pos between tiles 0-9
        self.food_pos = [positionX, positionY]              # food position is these x,y values combined
