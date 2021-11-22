import random
from Snake import Snake
from numpy.random import choice

# Summarizing this class:
# -- It will provide us with two selection methods: 1.Best Selection 2.Roulette Wheel Selection
# -- It will give us a mutation function for mutating the new offspring
# -- It will have two crossover functions: 1.Crossover Each Neuron 2.Crossover Midpoint
# -- Basic fitness calculation and initiating population functions
class GeneticAlgorithm:

    # use a function to return a random mutation intensity. If its big the change is heavy otherwise its small
    def mutation_factor(self):
        return 1 + ((random.random() - 0.5) * 3 + (random.random() - 0.5))

    # this mutate function will try to mutate every weight of the snake
    def mutate(self, matrix, mutation_rate):
        for element in matrix:              # for every W1, W2 etc.
            for i in range(matrix[element].shape[0]):       # for every row in this W
                for j in range(matrix[element].shape[1]):   # for every column in this W
                    if random.random() < mutation_rate:     # if the random number is found less then apply the mutation
                        matrix[element][i][j] *= self.mutation_factor()             # mutation intensity is determined with a function
        return matrix       # in the end return the mutated matrix

    # difference between the two crossover methods is this:
    # --crossover_each_neuron method copies random weights W1[i][j] from each parent
    # --crossover_midpoint method takes a random midpoint and copies left side from one parent and right side from other parent
    # you must pick one of the two

    def crossover_each_neuron(self, parent1, parent2):
        brain_size = len(parent1.brain.parameters) // 2
        child = Snake([])           # create a new snake that will inherit from parent

        for index in range(1,brain_size+1):
            col_len = len(parent1.brain.parameters["W" + str(index)][0])
            row_len = len(parent1.brain.parameters["W" + str(index)])
            for i in range(row_len):
                for j in range(col_len):
                    parent = random.choice([parent2, parent1])
                    child.brain.parameters["W" + str(index)][i][j] = parent.brain.parameters["W" + str(index)][i][j]
                #for j in range(col_len):
                #    parent = random.choice([parent2, parent1])
                #    child.brain.parameters["b" + str(index)][0][j] = parent.brain.parameters["b" + str(index)][0][j]

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
            #child.brain.parameters["b" + str(index)][:][:midpoint] = parents[0].brain.parameters["b" + str(index)][:midpoint]
            child.brain.parameters["W" + str(index)][midpoint:] = parents[1].brain.parameters["W" + str(index)][midpoint:]
            #child.brain.parameters["b" + str(index)][:][midpoint:] = parents[0].brain.parameters["b" + str(index)][midpoint:]
        return child

    # fitness is the probability that a snake gets choosen to create offspring
    def calculate_fitness(self,snakes):
        sum = 0
        # sum all of the snakes scores
        for snake in snakes:
            sum += snake.score

        # calculate how much snake contributed to the total score and that is our fitness
        for snake in snakes:
            snake.fitness = snake.score / sum

        return snakes


    def roulette_wheel(self, snakes, parent_ratio = 0.2, random_ratio = 0.1, breed_ratio=0.8, mutation_rate=0.07):
        choosen = []

        pop_size = len(snakes)
        parent = int(parent_ratio * pop_size)
        breed = int(breed_ratio * pop_size)
        rand = int(random_ratio * pop_size)             # how many random snakes will be selected

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
            new_snake.brain.parameters = self.mutate(new_snake.brain.parameters, mutation_rate)     # mutate the child
            choosen.append(new_snake)

        return choosen

    def best_selection(self, snakes, parent_ratio= 0.20, random_ratio = 0.1, breed_ratio = 0.7, mutation_rate = 0.15):
        choosen = []                # this is the list we will return at the end which holds the new created population
        best_to_worst = sorted(snakes, key= lambda x: x.score, reverse=True)    # sort the dead snakes list based on their score
        pop_size = len(snakes)
        parent = int(parent_ratio * pop_size)           # how many parents will be selected
        breed = int(breed_ratio * pop_size)             # how many childs will be produced
        rand = int(random_ratio * pop_size)             # how many random snakes will be selected

        # parents are picked from the best_to_worst list sequantially
        for i in range(parent):
            curr_snake_brain = best_to_worst[i].brain.parameters
            new_snake = Snake(curr_snake_brain)
            choosen.append(new_snake)

        # breeding the snakes from the parents
        for i in range(breed):
            parentA = random.choice(choosen)
            parentB = random.choice(choosen)
            new_snake = self.crossover_each_neuron(parentA, parentB)           # using midpoint crossover method
            new_snake.brain.parameters = self.mutate(new_snake.brain.parameters, mutation_rate)     # mutate the child
            choosen.append(new_snake)

        # random snakes are picked to keep diversity
        for i in range(rand):
            index = random.randint(0,pop_size-1)
            rand_snake_brain = snakes[index].brain.parameters
            new_snake = Snake(rand_snake_brain)
            choosen.append(new_snake)
        # return the newly created population
        return choosen

    # choose a snake based on its fitness
    def choose(self, snakes, fitness):
        new_snake = choice(a=snakes,size=1,p=fitness)       # returns [new_snake] so we must new_snake[0] to reach to snake
        new_snake[0].reset()                                # reset the snake because it has class variables set to some values like counter = 60 for example
        return new_snake[0]

    # create a population at the start of the game snakes is the list we add the created snakes to
    def initiate_population(self, snakes, n_snakes):
        for _ in range(n_snakes):                          # n_snakes is how many snakes will be created
            new_snake = Snake([])
            snakes.append(new_snake)
        return snakes


