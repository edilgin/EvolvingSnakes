import random
from Snake import Snake
from numpy.random import choice

class GeneticAlgorithm:

    def mutation_factor(self):
        return 1 + ((random.random() - 0.5) * 3 + (random.random() - 0.5))

    def mutate(self, matrix, mutation_rate):
        for element in matrix:
            for i in range(matrix[element].shape[0]):
                for j in range(matrix[element].shape[1]):
                    if random.random() < mutation_rate:
                        matrix[element][i][j] *= self.mutation_factor()
        return matrix

    def crossover_each_neuron(self, parent1, parent2):        # both parents are instances of class snake
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

    def crossover_midpoint(self, parent1, parent2):        # both parents are instances of class snake
        brain_size = len(parent1.brain.parameters) // 2
        child = Snake([])
        for index in range(1,brain_size+1):
            col_len = len(parent1.brain.parameters["W" + str(index)][0])
            midpoint = random.randint(0,col_len-1)
            parents = [parent2, parent1]
            random.shuffle(parents)
            child.brain.parameters["W" + str(index)][:midpoint] = parents[0].brain.parameters["W" + str(index)][:midpoint]
            child.brain.parameters["b" + str(index)][:][:midpoint] = parents[0].brain.parameters["b" + str(index)][:midpoint]
            child.brain.parameters["W" + str(index)][midpoint:] = parents[1].brain.parameters["W" + str(index)][midpoint:]
            child.brain.parameters["b" + str(index)][:][midpoint:] = parents[0].brain.parameters["b" + str(index)][midpoint:]
        return child


    def calculate_fitness(self,snakes):
        sum = 0
        for snake in snakes:
            sum += snake.score

        for snake in snakes:
            snake.fitness = snake.score / sum

        return snakes


    def roulette_wheel(self, snakes, parent_ratio = 0.2, breed_ratio=0.8, mutation_rate=0.07):
        choosen = []

        pop_size = len(snakes)
        parent = int(parent_ratio * pop_size)
        breed = int(breed_ratio * pop_size)

        snakes = self.calculate_fitness(snakes)
        scores = [snake.score for snake in snakes]
        fitness_list = [snake.fitness for snake in snakes]
        print("avg: ", sum(scores) / len(scores), "\n")
        for i in range(parent):
            curr_snake = self.choose(snakes, fitness_list)
            curr_snake.reset()
            choosen.append(curr_snake)

        for i in range(breed):
            parentA = random.choice(choosen)
            parentB = random.choice(choosen)
            new_snake = self.crossover_each_neuron(parentA, parentB)
            choosen.append(new_snake)

        for i in range(len(choosen)):
            new_snake = choosen[i]
            if random.random() < mutation_rate:
                new_snake.brain.parameters = self.mutate(new_snake.brain.parameters, mutation_rate)

        return choosen

    def best_selection(self, snakes, parent_ratio= 0.2, random_ratio = 0.1, breed_ratio = 0.7, mutation_rate = 0.12):
        choosen = []
        best_to_worst = sorted(snakes, key= lambda x: x.score, reverse=True)
        pop_size = len(snakes)
        parent = int(parent_ratio * pop_size)
        breed = int(breed_ratio * pop_size)
        rand = int(random_ratio * pop_size)

        for i in range(parent):
            curr_snake_brain = best_to_worst[i].brain.parameters
            curr_snake_brain = self.mutate(curr_snake_brain, mutation_rate)
            new_snake = Snake(curr_snake_brain)
            choosen.append(new_snake)

        for i in range(rand):
            index = random.randint(0,pop_size-1)
            rand_snake_brain = snakes[index].brain.parameters
            new_snake = Snake(rand_snake_brain)
            choosen.append(new_snake)


        for i in range(breed):
            parentA = random.choice(choosen)
            parentB = random.choice(choosen)
            new_snake = self.crossover_midpoint(parentA, parentB)
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


