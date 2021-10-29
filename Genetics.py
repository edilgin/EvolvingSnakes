import random
from Snake import Snake
from numpy.random import choice

class GeneticAlgorithm:
    @staticmethod
    def mutate(matrix, mutation_rate):
        mutation = random.randint(0, 100)
        if mutation < mutation_rate * 100:
            keys = list(matrix.keys())
            rand_element = random.choice(keys)
            rand_row = random.randint(0, len(matrix[rand_element])-1)
            rand_col = random.randint(0,len(matrix[rand_element][0])-1)
            matrix[rand_element][rand_row][rand_col] = random.randint(-2,2)
        return matrix

    def crossover(self, parent1, parent2):        # both parents are instances of class snake
        brain_size = len(parent1.brain.parameters) // 2
        child = Snake([])
        for index in range(1,brain_size+1):
            col_len = len(parent1.brain.parameters["W" + str(index)][0])
            row_len = len(parent1.brain.parameters["W" + str(index)])
            for j in range(col_len):
                parent = random.choice([parent2, parent1])
                for i in range(row_len):
                    child.brain.parameters["W" + str(index)][i][j] = parent.brain.parameters["W" + str(index)][i][j]
                    child.brain.parameters["b" + str(index)][0][j] = parent.brain.parameters["b" + str(index)][0][j]
            
        return child

    def calculate_fitness(self,snakes):
        sum = 0
        for snake in snakes:
            sum += snake.score

        for snake in snakes:
            snake.fitness = snake.score / sum


    def roulette_wheel(self, snakes, breed_ratio=0.7, mutation_rate=0.1):
        self.calculate_fitness(snakes)
        choosen = []

        pop_size = len(snakes)
        parents = int((1-breed_ratio) * pop_size)
        breed = int(breed_ratio * pop_size)

        fitness_list = [snake.fitness for snake in snakes]
        for i in range(parents//2):
            new_snake = self.choose(snakes, fitness_list)
            new_snake.reset()
            choosen.append(new_snake)

        for i in range(parents//2):
            s = self.choose(snakes, fitness_list)
            new_s = Snake([])
            new_s.brain.parameters = self.mutate2(s.brain.parameters, 0.07)
            choosen.append(new_s)

        #choosen = self.mutate3(choosen, 2, 7.0)
        for i in range(breed):
            parentA = random.choice(choosen)
            parentB = random.choice(choosen)
            snake = self.crossover(parentA, parentB)
            snake.brain.parameters = self.mutate2(snake.brain.parameters, 0.07)
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
            new_brain = self.mutate2(top_snakes[i].brain.parameters, mutation_rate)
            new_snake = Snake(new_brain)
            choosen.append(new_snake)

        # add some random snakes to not get stuck in local minima
        for i in range(rand):
            index = random.randint(0,len(snakes)-1)
            brain = snakes[index].brain.parameters
            new_snake = Snake(brain)
            choosen.append(new_snake)

        return choosen

    def initiate_population(self, snakes, n_snakes):
        for _ in range(n_snakes):
            new_snake = Snake([])
            snakes.append(new_snake)
        return snakes


    @staticmethod
    def mutate2(matrix, mutation_rate):
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
