import random

import numpy as np
from NonDominatedSet import NonDominatedSet


class AntColonyOptimization:

    def __init__(self, problem, num_ants=10, alpha=1.0, beta=2.0, evaporation_rate=0.5, max_iterations=50):
        self.problem = problem
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.max_iterations = max_iterations
        self.pheromone_matrix = self.initialize_pheromones()

    # initial the pheromones matrix
    def initialize_pheromones(self):
        return np.ones((self.problem.numOfCities, self.problem.numOfCities))

    # generate the Heuristic Matrix by the distance
    def generate_Heuristic_Matrix(self):
        heuristicMatrix = np.zeros((self.problem.numOfCities, self.problem.numOfCities))
        for i in range(self.problem.numOfCities):
            for j in range(self.problem.numOfCities):
                if i != j:
                    if self.problem.distanceMatrix[i][j] != 0:
                        heuristicMatrix[i][j] = round(1 / self.problem.distanceMatrix[i][j], 4)
                else:
                    heuristicMatrix[i][j] = 0

        return heuristicMatrix

    # Repair the picking scheme. Ensure the total weight not over the maxWeight
    def update_flags(self, z):
        total_weight = 0
        for i in range(len(z)):
            if z[i]:
                total_weight += self.problem.itemMatrix[i][0]
        while total_weight > self.problem.maxWeight:
            index = random.randint(0, self.problem.numOfCities - 1)
            if z[index]:
                total_weight -= self.problem.itemMatrix[index][0]
                z[index] = 0
        return z

    # The process of the ACO Algorithm
    def solve(self):
        nds = NonDominatedSet()
        print(self.problem.itemMatrix)
        heu_matrix = self.generate_Heuristic_Matrix()
        for iteration in range(self.max_iterations):
            ant_tours = []
            for ant in range(self.num_ants):
                tour = []
                current_city = 0
                for _ in range(self.problem.numOfCities):
                    tour.append(current_city)
                    numerators = []
                    probabilities = []
                    sum_numerator = 0
                    sum_cumulative_pro = 0
                    cumulative_pros = []
                    for city in range(self.problem.numOfCities):
                        if city not in tour:
                            pheromone_factor = self.pheromone_matrix[current_city, city] ** self.alpha
                            heuristic_factor = heu_matrix[current_city, city] ** self.beta
                            numerator = pheromone_factor * heuristic_factor
                            numerators.append((city, numerator))
                            sum_numerator += numerator
                    for i in numerators:
                        if sum_numerator != 0:
                            probability = i[1] / sum_numerator
                            probabilities.append((i[0], probability))
                    for i in probabilities:
                        sum_cumulative_pro += i[1]
                        cumulative_pros.append((i[0], sum_cumulative_pro))
                    # generate a number between 0 and 1, compare to the cumulative probabilities, decide the next city
                    random_value = random.uniform(0, 1)
                    for i in cumulative_pros:
                        if i[1] > random_value:
                            current_city = i[0]
                            break
                ant_tours.append(tour)
            for i in range(self.problem.numOfCities):
                for j in range(self.problem.numOfCities):
                    self.pheromone_matrix[i][j] *= 1 - self.evaporation_rate
            # Iterate over all paths in each generation
            for path in ant_tours:
                # # generate the list of flag to decide to pick or not for each city
                flag = random.choices([0, 1], weights=[0.3, 0.7], k=self.problem.numOfCities)
                # repair the list of the picking scheme
                z = self.update_flags(flag)
                # calculate the solution with the path and the picking scheme
                solution = self.problem.fitnessFunction(path, z)
                # Updating the pheromone matrix
                delta = (1 / solution.time) * solution.profit
                for i in path:
                    self.pheromone_matrix[i - 1][i] += delta
                print(solution.objectives)
                # Add the solution to the non-dominate set
                nds.add(solution)
                # A local search method that try more picking scheme for the same path
                for a in range(1, 100):
                    weight0 = a / 100
                    weight1 = 1 - weight0
                    for _ in range(20):
                        num_zeros = int(self.problem.numOfCities * weight0)
                        num_ones = self.problem.numOfCities - num_zeros
                        flag = [0] * num_zeros + [1] * num_ones
                        random.shuffle(flag)
                        z = self.update_flags(flag)
                        solution = self.problem.fitnessFunction(path, z)
                        print(solution.objectives)
                        nds.add(solution)

        return nds.entries
