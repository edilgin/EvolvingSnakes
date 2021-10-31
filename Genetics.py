import random
from Snake import Snake
from numpy.random import choice

class GeneticAlgorithm:
    @staticmethod
    def mutate(matrix, mutation_rate):
        for element in matrix:
            arr = matrix[element]
            for i in range(arr.shape[0]):
                for j in range(arr.shape[1]):
                    mutation = random.randint(0, 100)
                    if mutation < mutation_rate*100:
                        rand_num = random.uniform(-0.1, 0.1)
                        arr[i][j] += rand_num
            matrix.update({element: arr})
        return matrix

    def crossover(self, parent1, parent2):        # both parents are instances of class snake
        brain_size = len(parent1.brain.parameters) // 2
        child = Snake([])
        for index in range(1,brain_size+1):
            col_len = len(parent1.brain.parameters["W" + str(index)][0])
            row_len = len(parent1.brain.parameters["W" + str(index)])
            for i in range(row_len):
                for j in range(col_len):
                    parent = random.choice([parent2, parent1])
                    child.brain.parameters["W" + str(index)][i][j] = parent.brain.parameters["W" + str(index)][i][j]
                for j in range(col_len):
                    parent = random.choice([parent2, parent1])
                    child.brain.parameters["b" + str(index)][0][j] = parent.brain.parameters["b" + str(index)][0][j]

        return child

    def calculate_fitness(self,snakes):
        sum = 0
        for snake in snakes:
            sum += snake.score

        for snake in snakes:
            snake.fitness = snake.score / sum


    def roulette_wheel(self, snakes, parent_ratio = 0.3, breed_ratio=0.7, mutation_rate=0.15):
        self.calculate_fitness(snakes)
        choosen = []

        pop_size = len(snakes)
        parent = int(parent_ratio * pop_size)
        breed = int(breed_ratio * pop_size)

        fitness_list = [snake.fitness for snake in snakes]
        for i in range(parent):
            curr_snake = self.choose(snakes, fitness_list)
            #new_snake = Snake(curr_snake.brain.parameters)
            curr_snake.reset()
            choosen.append(curr_snake)

        for i in range(breed):
            parentA = random.choice(choosen)
            parentB = random.choice(choosen)
            new_snake = self.crossover(parentA, parentB)
            new_snake.brain.parameters = self.mutate(new_snake.brain.parameters, mutation_rate)
            choosen.append(new_snake)

        return choosen

    def choose(self, snakes, fitness):
        new_snake = choice(a=snakes,size=1,p=fitness)
        new_snake[0].reset()
        return new_snake[0]

    def initiate_population(self, snakes, n_snakes):
        for _ in range(n_snakes):
            new_snake = Snake([])
            snakes.append(new_snake)
        return snakes


