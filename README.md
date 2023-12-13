# README: Traveling Thief Problem (TTP) with Genetic Algorithm and Ant Colony Optimiztion

 

# Overview

The purpose of this project is to attempt to solve the TTP. We implement two separate algorithms: Ant Colony Optimization (ACO) and a GA algorithm to solve the problem.

 

# Prerequisites

\- Python 3. 11;

\- Required Python libraries: ‘numpy’, ‘re’, ‘os’ 'random' and 'time'. 

 

## Usage

1. Clone or download the program files to your local machine.

2. Examples of data files include the following files. We control the use of a single or specified data file to perform experiments by adding comment symbols.

   ```python
   Instances = [
               # "test-example-n4",
               # a280_n279_bounded-strongly-corr_01.ttp
               "a280-n279",
               # a280_n1395_uncorr-similar-weights_05.ttp
               # "a280-n1395",
               # a280_n2790_uncorr_10.ttp
               # "a280-n2790",
               # # fnl4461_n4460_bounded-strongly-corr_01.ttp
               # "fnl4461-n4460",
               # # fnl4461_n22300_uncorr-similar-weights_05.ttp
               # "fnl4461-n22300",
               # # fnl4461_n44600_uncorr_10.ttp
               # "fnl4461-n44600",
               # pla33810_n33809_bounded-strongly-corr_01.ttp
               # "pla33810-n33809",
               # pla33810_n169045_uncorr-similar-weights_05.ttp
               # "pla33810-n169045",
               # pla33810_n338090_uncorr_10.ttp
               # "pla33810-n338090"
   ]
   ```

3. Regarding the ACO algorithm, we can modify the number of ants and the maximum number of iterations(AntColonyOptimization.py) to determine the termination condition.

   ```python
   class AntColonyOptimization:
   
       def __init__(self, problem, num_ants=10, alpha=1.0, beta=2.0, evaporation_rate=0.5, max_iterations=50):
           self.problem = problem
           self.num_ants = num_ants
           self.alpha = alpha
           self.beta = beta
           self.evaporation_rate = evaporation_rate
           self.max_iterations = max_iterations
           self.pheromone_matrix = self.initialize_pheromones()
   ```

4. Regarding the GA algorithm, we can improve the efficiency of the operation for different data files by modifying the number of populations, the tournament selection size, and the maximum number of iterations(GeneticAlgorithm.py).

   ```python
   class GeneticAlgorithm:
   
       def __init__(self, problem):
           self.problem = problem
           self.population_size = 50
           self.tournament_size = 5
           self.numSelect = 2
           self.termination_criterion = 100
           self.population = None
           self.flag = None
   ```

5. Control the execution of different algorithms by annotating or releasing the corresponding algorithm execution statements(Runner.py).

   ```python
   # Creating ACO Algorithm Objects
   aco_algorithm = ACO(problem)
   # Call the ACO algorithm and return the non-dominated set
   nds = aco_algorithm.solve()
   # Creating GA Algorithm Objects
   # ga_algorithm = GA(problem)
   # Call the GA algorithm and return the non-dominated set
   # nds = ga_algorithm.solve() 
   ```

6. The results are saved to the appropriate data file according to the contest criteria. and stored in a folder named results. Like this: 

  ![image](https://github.com/najeeb-yusuf/traveling-thief-problem/assets/150862149/9ffa4ff6-551c-42a6-8014-e49b1ebea079)


   

# Parameters

ACO Algorithm:

- num_ants: The number of ants.

- alpha: The hyper parameter of the pheromone matrix

- beta: The hyper parameter of the heuristic matrix

- evaporation_rate: the rate of evaporation

- max_iterations: The number of generations for the algorithm to run

GA Algorithm:

- ‘Pop_size’: Initial population size.

- ‘Tour_size’: Tournament selection sample size.

- ‘Termination_Criterion’: The number of generations for the algorithm to run.

By modifying the variable values above, different data experiments have been conducted.

 

## Program Components

- readTxtFile: Read the data from the data file

- getDistanceMatrix: Initialize the distance matrix

- getDistance: Get the distance values between cities from the distance matrix

- getItemMatrix: Items are filtered by localsearch, generating the weight of the item as well as a profit matrix. Filter items by setting a queue on the ratio of weight to profit.

- ACO:

  - generate_Heuristic_Matrix: Initializing the heuristic matrix using the distance
  - initialize_pheromones: Initializing the pheromones matrix 
  - update_flags: Optimise the list of flags for pickup scenarios to ensure that the pack weight limit is met before calculating fitness
  - solve: ACO algorithm implementation

- GA:

  - initialize_population: Generating the initial population
  - initialize_flag: Generating the initial flag list
  - update_flags: Optimize the list of flags for pickup scenarios to ensure that the pack weight limit is met before calculating fitness
  - tournament_selection: Generation of parent samples by tournament selection strategy
  - order_crossover: Crossover the path
  - crossover_flag: Crossover the list of flag
  - inversion_mutation: Reverse mutation of paths and the list of flag
  - repalcement: Renewal of populations.

- Non-Dominate Set:

  add & get_relation: Used to check the generated results and generate non-dominated sets

- write_solutions: Data is stored according to the requirements of the competition and saved to the appropriate data file.

- print_solutions: Print the final generated solution

   

## Output

- The program will display the path found, the picking scheme, its time, profit and execution time.

- The results will be saved in a text file named "team_name_problem_name.x" or"team_name_problem_name.f"

  - "team_name_problem_name.f": Save time and profit

  - "team_name_problem_name.x": Save paths and item picking scheme

    Like this:
![image](https://github.com/najeeb-yusuf/traveling-thief-problem/assets/150862149/1fbaaf79-62f1-494a-88f1-a34104c7b6fe)
![image](https://github.com/najeeb-yusuf/traveling-thief-problem/assets/150862149/66417194-bbdd-4694-8447-c9cb40a5cc83)


    

 

## Example

If don't need the set the parameters that you want, just run the python file(Runner.py)

![image](https://github.com/najeeb-yusuf/traveling-thief-problem/assets/150862149/acb6e5a6-19be-4e5c-8759-05d642309143)



 

## Authors

\- Nature Inspired Computation - GROUP N

- WILKINSON, Charlie
- RAHATAL, Ritesh Sunil

- JIN, Hongjin

- WANG, Peitao

- YUSUF, Najeeb

- LIU, Sihang

 

## Acknowledgments

\- The program is based on the concept of Genetic Algorithm, Ant Colony Optimal and the Traveling Thief Problem.

 
