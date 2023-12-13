import os
import time
from Utils import readTxtFile, write_solutions, print_solutions
from AntColonyOptimization import AntColonyOptimization as ACO
from GeneticAlgorithm import GeneticAlgorithm as GA

# List of instances
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

start = time.time()
for instance in Instances:
    # Read the datafile. Get the matrix of the distance and the items of the cities
    problem = readTxtFile(instance)
    # Creating ACO Algorithm Objects
    aco_algorithm = ACO(problem)
    # Call the ACO algorithm and return the non-dominated set
    nds = aco_algorithm.solve()
    # Creating GA Algorithm Objects
    # ga_algorithm = GA(problem)
    # Call the GA algorithm and return the non-dominated set
    # nds = ga_algorithm.solve() 
    print('Non-dominate:')
    for s in nds:
        print(s.time, s.profit, s.weight)
    # Sort the solutions of the non-dominated set by temporal attributes
    nds_sorted = sorted(nds, key=lambda nds: nds.time)
    print('sorted:')
    for s in nds_sorted:
        print(s.time, s.profit, s.weight)
    # Print the complete solution to the console, including routes, item pickup schedules, times, and profits
    print_solutions(nds_sorted, True)
    # Save the data results to the specified results folder
    # store them in a file of the appropriate format as required
    folder_path = 'result'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    write_solutions(folder_path, team_name='NIC-GROUP N', problem_name=problem.name, solutions=nds_sorted)

end = time.time()
print(end - start)


