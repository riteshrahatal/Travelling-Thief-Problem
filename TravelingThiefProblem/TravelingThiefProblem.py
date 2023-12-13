import math

import numpy as np

from Solution import Solution


# Calculate the distance between two points by Euclid's formula
def euclideanDistance(city1, city2):
    return math.sqrt((city2[0] - city1[0]) ** 2 + (city2[1] - city1[1]) ** 2)


# Filtering of the city's items by the ratio of weight and profit to the set queue value
def find_max_profit(weights, profits):
    total_weight = 0
    total_profit = 0
    for i in range(len(weights)):
        if weights[i] / profits[i] < 200:
            total_weight += weights[i]
            total_profit += profits[i]
    return total_weight, total_profit


# encapsulated data
class TravelingThiefProblem:
    def __init__(self):
        self.name = None  # filename
        self.numOfCities = -1  # dimension -> number of city
        self.numOfItem = -1  # number of items
        self.minSpeed = -1  # min speed
        self.maxSpeed = -1  # max speed
        self.maxWeight = -1  # capacity of knapsack
        self.R = float('inf')  # renting ratio
        self.coordinates = None  # the coordinate of nood
        self.weight = None  # Weight of items of each city
        self.profit = None  # Profit of items of each city
        self.distanceMatrix = None  # Record the distance matrix between cities
        self.itemMatrix = None  # Record the weight and profit of items picked up in each city

    # Calculate the distance matrix
    def getDistanceMatrix(self):
        self.distanceMatrix = np.zeros((self.numOfCities, self.numOfCities))
        for i in range(self.numOfCities):
            for j in range(self.numOfCities):
                self.distanceMatrix[i][j] = euclideanDistance(self.coordinates[i], self.coordinates[j])

    # Getting distance values in the distance matrix by city coordinates
    def getDistance(self, cityIndex_1, cityIndex_2):
        return self.distanceMatrix[cityIndex_1 - 1][cityIndex_2 - 1]

    # Filtering of items for the city returns minimum weight and maximum profit
    def searchItem(self, cityIndex):
        weights = self.weight[cityIndex - 1]
        profits = self.profit[cityIndex - 1]
        minWeight, maxProfit = find_max_profit(weights, profits)
        return minWeight, maxProfit

    # Filtering city items to obtain item matrices
    def getItemMatrix(self):
        self.itemMatrix = []
        for i in range(1, self.numOfCities + 1):
            minWeight, maxProfit = self.searchItem(i)
            self.itemMatrix.append([minWeight, maxProfit])
        self.itemMatrix[0] = [0, 0]

    # update the speed through the formula with the current weigth
    def update_speed(self, u_weight):
        if u_weight < self.maxWeight:
            return self.maxSpeed - (u_weight / self.maxWeight) * (self.maxSpeed - self.minSpeed)
        else:
            return self.minSpeed

    # Get the solution based on the path as well as the pickup plan
    def fitnessFunction(self, path, z):
        total_weight = 0
        total_time = 0
        total_profit = 0
        for i in range(len(path) - 1):
            city_start = path[i] - 1
            city_end = path[i + 1] - 1
            speed = self.update_speed(total_weight)
            if z[city_end]:
                total_weight += self.itemMatrix[city_end][0]
                total_profit += self.itemMatrix[city_end][1]
            total_time += self.getDistance(city_start, city_end) / speed

        speed = self.update_speed(total_weight)
        total_time += self.getDistance(self.numOfCities - 1, 0) / speed

        solution = Solution()
        solution.path = path
        solution.z = z
        solution.profit = total_profit
        solution.time = total_time
        solution.objectives = [total_time, -total_profit]
        solution.single_objective = total_profit - self.R * total_time
        solution.weight = total_weight
        return solution
