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

    fitness_dict["child1"] = [mutated_children[0], int(child1_fitness)]
    fitness_dict["child2"] = [mutated_children[1], int(child2_fitness)]

    return fitness_dict




def ga_call(generations, percent_population_selected, population_size,progress_file_name, results_file_name):
    """ Function calls the genetic algorithm for the amount of times specified. """
    pop = int(population_size / 2)
    # create parents
    parent1 = random.sample(range(8), 8)
    parent2 = random.sample(range(8), 8)
    open_progress_file = open(progress_file_name, 'w')
    most_fit_path = []
    most_fit_score = 10000000

    # Complete as my iterations as there are generations
    for generation in range(1, generations + 1):
        # divide population size by 2 since each crossover results in 2 children, only need to call function 50 xs
        population_dict = {}
        child_num = 1
        for i in range(pop):
            # perform Crossover
            children = crossover(parent1, parent2)

            # perform mutation
            mutated_children = mutation(children)

            # calculate fitness
            fitness_dict = fitness(mutated_children)
            for key, value in fitness_dict.items():
                population_dict["Child " + str(child_num)] = value
                child_num+=1

        df = pd.DataFrame(population_dict)
        df.index = ["path", "fitness"]
        df = df.transpose()
        sub_set = df.sort_values(by="fitness", ascending=True)[:40]
        smallest_of_sub = sub_set.iloc[[0]]

        if smallest_of_sub["fitness"][0] < most_fit_score:
            most_fit_score = smallest_of_sub["fitness"][0]
            most_fit_path = smallest_of_sub["path"][0]

        average_fitness_scores = sub_set["fitness"].mean()
        median_fitness_scores = sub_set["fitness"].median()
        std_fitness_scores = sub_set["fitness"].std()
        open_progress_file.write(str(generation) + ". " + "Population Size: " + str(population_size) + " for iteration " + str(generation) + "\n")
        open_progress_file.write("Average fitness scores " + str(average_fitness_scores) + "\n")
        open_progress_file.write("Median fitness scores " + str(median_fitness_scores) + "\n")
        open_progress_file.write("STD fitness scores " + str(std_fitness_scores) + "\n")
        open_progress_file.write("Size of the selected subset of the population " + str(percent_population_selected) + "\n\n")

    best_city_list = []
    for city in most_fit_path:
        best_city_list.append(index_dict[city])

    open_result_file = open(results_file_name, 'w')
    for i in range(len(most_fit_path)):
        open_result_file.write(str(most_fit_path[i]) + " " + best_city_list[i] + "\n")

    open_result_file.close()
    open_progress_file.close()



distance_matrix_path = 'TS_Distances_Between_Cities.csv'
generations = 50
percent_population_selected = 40
population_size = 100
progress_file_name = "Eden_Johnson_GA_TS_Info.txt"
results_file_name = "Eden_Johnson_GA_TS_Result.txt"

ga_call(generations, percent_population_selected, population_size, progress_file_name, results_file_name)