import pandas as pd
import numpy as np
import random, operator

distance_csv = pd.read_csv('TS_Distances_Between_Cities.csv', ',', index_col=0)
distance_df = distance_csv.dropna()
cities_dict = distance_df.to_dict()
cities = distance_df.columns.to_list()

index_dict = {}
for i in range(len(cities)):
    index_dict[i] = cities[i]


# perform Crossover
parent1 = [0, 1, 2, 3, 4, 5, 6, 7]
parent2 = [7, 6, 5, 4, 3, 2, 1, 0]

def crossover(parent1, parent2):
    """ Performs crossover between two parents and returns a child. """

    window_size = random.randint(0, 7)
    possible_starting_index = random.randint(0, (len(parent1) - window_size + 1))

    child = []
    for i in range(len(parent1)):
        child.append("-")

    child[possible_starting_index:(possible_starting_index + window_size)] = parent1[possible_starting_index:(possible_starting_index + window_size)]

    values_to_add = []

    for i in range(len(parent2)):
        if parent2[i] not in child:
            values_to_add.append(parent2[i])

    for i in range(len(child)):
        if child[i] == "-":
            child[i] = values_to_add.pop(0)

    return child

child = crossover(parent1, parent2)
print(child)

# perform mutation
def mutation(child):
    """ Performs point switch mutation on a child and returns the mutated child. """
    possible_first_index = random.randint(0, 7)
    possible_second_index = random.randint(0, 7)
    first_value = child[possible_first_index]
    second_value = child[possible_second_index]
    child[possible_first_index] = second_value
    child[possible_second_index] = first_value
    return child

mutated_child = mutation(child)
print(mutated_child)

new_city_list = []
for i in range(len(mutated_child)):
    city = index_dict[mutated_child[i]]
    new_city_list.append(city)


fitness_score = 0
# look up distance metrics for child in table
for i in range(len(new_city_list) - 1):
    fitness_score += distance_df[new_city_list[i]][i + 1]

print(fitness_score)

def ga_call(generations, percent_population_selected, population_size):
    """ Function calls the genetic algorithm for the amount of times specified. """

distance_matrix_path = 'TS_Distances_Between_Cities.csv'
generations = 50
percent_population_selected = 40
population_size = 100
progress_file_name = "Eden_Johnson_GA_TS_Info.txt"
results_file_name = "Eden_Johnson_GA_TS_Result.txt"

