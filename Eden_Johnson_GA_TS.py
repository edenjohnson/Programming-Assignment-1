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
    """ Performs crossover between two parents and returns 2 children. """

    window_size = random.randint(0, 7)
    possible_starting_index = random.randint(0, (8 - window_size + 1))

    child1 = []
    child2 = []
    for i in range(8):
        child1.append("-")
        child2.append("-")

    child1[possible_starting_index:(possible_starting_index + window_size)] = parent1[possible_starting_index:(possible_starting_index + window_size)]
    child2[possible_starting_index:(possible_starting_index + window_size)] = parent2[possible_starting_index:(possible_starting_index + window_size)]

    values_to_add_child_1 = []
    values_to_add_child_2 = []

    for i in range(len(parent2)):
        if parent2[i] not in child1:
            values_to_add_child_1.append(parent2[i])
        if parent1[i] not in child2:
            values_to_add_child_2.append(parent1[i])

    for i in range(len(child1)):
        if child1[i] == "-":
            child1[i] = values_to_add_child_1.pop(0)

    for i in range(len(child2)):
        if child2[i] == "-":
            child2[i] = values_to_add_child_2.pop(0)

    return [child1, child2]

children = crossover(parent1, parent2)

# perform mutation
def mutation(children):
    """ Performs point switch mutation on a child and returns the mutated child. """
    mutated_children = []
    for child in children:
        possible_first_index = random.randint(0, 7)
        possible_second_index = random.randint(0, 7)
        first_value = child[possible_first_index]
        second_value = child[possible_second_index]
        child[possible_first_index] = second_value
        child[possible_second_index] = first_value
        mutated_children.append(child)
    return mutated_children

mutated_children = mutation(children)

def fitness(mutated_children):
    """ Function takes in a list of mutated children and calculates their fitness. Stores data in a dictionary """
    fitness_dict = {}
    child1_fitness = 0
    child2_fitness = 0

    new_city_list_child_1 = []
    new_city_list_child_2 = []
    for i in range(len(mutated_children[0])):
        city = index_dict[mutated_children[0][i]]
        new_city_list_child_1.append(city)

    # look up distance metrics for child in table
    for i in range(len(new_city_list_child_1) - 1):
        child1_fitness += distance_df[new_city_list_child_1[i]][mutated_children[0][i + 1]]

    for i in range(len(mutated_children[1])):
        city = index_dict[mutated_children[1][i]]
        new_city_list_child_2.append(city)

    # look up distance metrics for child in table
    for i in range(len(new_city_list_child_2) - 1):
        child2_fitness += distance_df[new_city_list_child_2[i]][mutated_children[1][i + 1]]

    fitness_dict[mutated_children[0]] = child1_fitness
    fitness_dict[mutated_children[1]] = child2_fitness

    return fitness_dict

fitness_dict = fitness(mutated_children)



def ga_call(generations, percent_population_selected, population_size, progress_file_name, results_file_name):
    """ Function calls the genetic algorithm for the amount of times specified. """





distance_matrix_path = 'TS_Distances_Between_Cities.csv'
generations = 50
percent_population_selected = 40
population_size = 100
progress_file_name = "Eden_Johnson_GA_TS_Info.txt"
results_file_name = "Eden_Johnson_GA_TS_Result.txt"

