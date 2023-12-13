import random

from NonDominatedSet import NonDominatedSet
from Utils import readTxtFile


# ordered crossover for the list of the path
def order_crossover(father):
    child = []
    father1 = father[0].copy()
    father2 = father[1].copy()
    crossover_point = random.randint(0, len(father1) - 1)
    child_1 = father2[:crossover_point]
    child_2 = father1[:crossover_point]

    # Ensure no repeated cities in the child's path
    for city in father1:
        if city not in child_1:
            child_1.append(city)
    for city in father2:
        if city not in child_2:
            child_2.append(city)
    child.append(child_1)
    child.append(child_2)
    return child


# simple crossover for the list of picking scheme
def crossover_flag(father):
    child = []
    father1 = father[0].copy()
    father2 = father[1].copy()
    crossover_point = random.randint(0, len(father1) - 1)
    child_1 = father2[:crossover_point]
    child_2 = father1[:crossover_point]
    for city in father1[crossover_point:]:
        child_1.append(city)
    for city in father2[crossover_point:]:
        child_2.append(city)
    child.append(child_1)
    child.append(child_2)
    return child


# the inversion mutation for the path and the picking scheme
def inversion_mutation(child):
    path = child.copy()
    index1, index2 = random.sample(range(len(path)), 2)
    if index1 > index2:
        index1, index2 = index2, index1
    path[index1:index2 + 1] = reversed(path[index1:index2 + 1])
    return path


# find the minimum solution about the solutions
def find_min_solution(solutions):
    min_value = float('inf')
    index = 0
    for i in range(len(solutions)):
        if (1 / solutions[i].time) * solutions[i].profit < min_value:
            min_value = (1 / solutions[i].time) * solutions[i].profit
            index = i
    return index


# find the maximum solution about the solutions
def find_max_solution(solutions):
    max_value = 0
    index = 0
    for i in range(len(solutions)):
        if (1 / solutions[i].time) * solutions[i].profit > max_value:
            max_value = (1 / solutions[i].time) * solutions[i].profit
            index = i
    return solutions[index]


# replace the individual through the value of solution
def replacement(solutions, solution):
    min_index = find_min_solution(solutions)
    min_solution = solutions[min_index]
    if (1 / min_solution.time) * min_solution.profit < (1 / solution.time) * solution.profit:
        solutions[min_index] = solution
    return solutions


class GeneticAlgorithm:

    def __init__(self, problem):
        self.problem = problem
        self.population_size = 50
        self.tournament_size = 5
        self.numSelect = 2
        self.termination_criterion = 100
        self.population = None
        self.flag = None

    # initial population
    def initialize_population(self):
        self.population = []
        for pl in range(self.problem.numOfCities):
            path = [0] + random.sample(range(1, self.problem.numOfCities), self.problem.numOfCities - 1)
            self.population.append(path)

    # initial population
    def initialize_flag(self):
        self.flag = []
        for pl in range(self.problem.numOfCities):
            f = random.choices([0, 1], weights=[0.3, 0.7], k=self.problem.numOfCities)
            self.update_flags(f)
            self.flag.append(f)

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

    # Generate parent samples through tournament selection
    def tournament_selection(self):
        father_select_path = []
        father_select_flag = []

        for i in range(self.numSelect):
            best_solution = None
            tournament_p = []
            tournament_f = []
            fitness_value = float('inf')
            for m in range(self.tournament_size):
                index = random.randint(0, len(self.population) - 1)
                tournament_p.append(self.population[index])
                tournament_f.append(self.flag[index])
            for n in range(len(tournament_p)):
                solution = self.problem.fitnessFunction(tournament_p[n], tournament_f[n])

                if solution.time < fitness_value:
                    best_solution = solution
                    fitness_value = solution.time
            father_select_path.append(best_solution.path)
            father_select_flag.append(best_solution.z)
        return father_select_path, father_select_flag

    # the process the GA Algorithm
    def solve(self):
        results = []
        nds = NonDominatedSet()
        self.initialize_population()
        print(self.problem.itemMatrix)
        self.initialize_flag()
        solutions = []
        print('population:')
        for i in range(len(self.population)):
            solution = self.problem.fitnessFunction(self.population[i], self.flag[i])
            solutions.append(solution)
            print(solution.objectives)
        results.append(find_max_solution(solutions))
        for _ in range(self.termination_criterion):
            solution_child = []
            fathers_path, fathers_flag = self.tournament_selection()
            child_path = order_crossover(fathers_path)
            child_flag = crossover_flag(fathers_flag)

            for i in range(len(child_path)):
                child_path[i] = inversion_mutation(child_path[i])
                child_flag[i] = inversion_mutation(child_flag[i])
                child_flag[i] = self.update_flags(child_flag[i])
                solution = self.problem.fitnessFunction(child_path[i], child_flag[i])
                solution_child.append(solution)

            for i in range(len(solution_child)):
                solutions = replacement(solutions, solution_child[i])

            results.append(find_max_solution(solutions))

        for result in results:
            print(result.objectives)
            nds.add(result)

        return nds.entries


