import random
from SnakeGame import Snake
from numpy.random import choice
import copy

class GeneticAlgorithm:
    def __init__(self, cols, rows, node_size, snake_x, snake_y):
        self.cols = cols
        self.rows = rows
        self.node_size = node_size
        self.x = snake_x
        self.y = snake_y

    @staticmethod
    def mutate(matrix, mutation_rate):
        mutation = random.randint(0, 100)
        if mutation < mutation_rate * 100:
            keys = list(matrix.keys())
            rand_element = random.choice(keys)
            rand_row = random.randint(0, len(matrix[rand_element])-1)
            rand_col = random.randint(0,len(matrix[rand_element][0])-1)
            matrix[rand_element][rand_row][rand_col] = random.randint(-5,5)
        return matrix

    @staticmethod
    def mutate2(matrix, mutation_rate):
        for element in matrix:
            arr = matrix[element]
            for i in range(arr.shape[0]):
                for j in range(arr.shape[1]):
                    mutation = random.randint(0, 100)
                    if mutation < mutation_rate*100:
                        rand_num = random.uniform(-4, 4)
                        arr[i][j] = rand_num
            matrix.update({element: arr})
        return matrix

    def crossover(self, parent1, parent2):        # both parents are instances of class snake
        brain_size = len(parent1.brain.parameters) // 2
        child = Snake(self.rows, self.cols,[], self.node_size, self.x, self.y)
        for index in range(1,brain_size+1):
            col_len = len(parent1.brain.parameters["W" + str(index)][0])
            row_len = len(parent1.brain.parameters["W" + str(index)])
            for j in range(col_len):
                parent = random.choice([parent2, parent1])
                for i in range(row_len):
                    child.brain.parameters["W" + str(index)][i][j] = parent.brain.parameters["W" + str(index)][i][j]
                    child.brain.parameters["b" + str(index)][0][j] = parent.brain.parameters["b" + str(index)][0][j]
            
        return child

    def calculate_fitnes(self,snakes):
        sum = 0
        for snake in snakes:
            sum += snake.score

        for snake in snakes:
            snake.fitness = snake.score / sum


    def roulette_wheel(self, snakes, breed_ratio=0.3, mutation_rate=0.1):
        self.calculate_fitnes(snakes)
        choosen = []

        pop_size = len(snakes)
        parents = int((1-breed_ratio) * pop_size)
        breed = int(breed_ratio * pop_size)

        fitness_list = [snake.fitness for snake in snakes]
        for i in range(parents):
            new_snake = self.choose(snakes, fitness_list)
            new_snake.brain.parameters = self.mutate(new_snake.brain.parameters, mutation_rate)
            choosen.append(new_snake)

        for i in range(breed):
            parentA = random.choice(snakes)
            parentB = random.choice(snakes)
            snake = self.crossover(parentA, parentB)
            choosen.append(snake)

        return choosen

    def choose(self, snakes, fitness):
        new_snake = choice(a=snakes,size=1,p=fitness)
        new_snake[0].reset()
        return new_snake[0]

    def choose_snakes(self, snakes, pick_top_ratio=0.25,  apply_breed_ratio=0.3, rand_ratio=0.2, mutation_rate = 0.1):

        choosen = []

        pop_size = len(snakes)
        top = int(pick_top_ratio * pop_size)
        breed = int(apply_breed_ratio * pop_size)
        rand = int(rand_ratio * pop_size)

        sorted_snakes = sorted(snakes, key= lambda x: x.score)
        top_snakes = sorted_snakes[:top]
        choosen.extend(top_snakes)

        # breed these snakes to get the required breeding ratio
        for i in range(breed):
            parentA = random.choice(choosen)
            parentB = random.choice(choosen)
            snake = self.crossover(parentA, parentB)
            choosen.append(snake)

        for i in range(len(top_snakes)):
            new_brain = self.mutate(top_snakes[i].brain.parameters, mutation_rate)
            new_snake = Snake(self.rows, self.cols, new_brain, self.node_size, self.x, self.y)
            choosen.append(new_snake)

        # add some random snakes to not get stuck in local minima
        for i in range(rand):
            index = random.randint(0,len(snakes)-1)
            brain = snakes[index].brain.parameters
            new_snake = Snake(self.cols, self.rows, brain, self.node_size, self.x, self.y)
            choosen.append(new_snake)

        return choosen

    def initiate_population(self, snakes, n_snakes):
        for _ in range(n_snakes):
            new_snake = Snake(self.rows, self.cols, [], self.node_size, self.x, self.y)
            snakes.append(new_snake)
        return snakes