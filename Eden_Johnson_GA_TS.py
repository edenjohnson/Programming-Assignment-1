import pandas as pd
import numpy as np
import random, operator


distance_csv = pd.read_csv('TS_Distances_Between_Cities.csv', ',', index_col=0)
distance_df = distance_csv.dropna()
cities = distance_df.columns.to_list()
cities_index = []
index_dict = {}
for i in range(len(cities)):
    index_dict[i] = cities[i]
    cities_index.append(i)

def initial_population(population_size, population):
    """ Function takes in a population size and creates that many cities to visit and returns them in a list. """
    pop = [random.sample(population, len(population)) for i in range(population_size)]
    return pop

def assess_fitness(child):
    """ Function takes in a child (path) and calculates their fitness. Stores data in a list that is
        returned. """
    fitness_dict = {}
    child_distance = 0
    child_fitness = 0
    new_city_list_child_1 = []

    for i in range(len(child)):
        city = index_dict[child[i]]
        new_city_list_child_1.append(city)

    # look up distance metrics for child in table
    for i in range(len(new_city_list_child_1) - 1):
        child_distance += distance_df[new_city_list_child_1[i]][child[i + 1]]

    child_fitness = 1 / float(child_distance)
    fitness_list = [child, child_fitness, child_distance]
    return fitness_list


def rank_routes(population):
    """ Function assesses the fitness of each member of the population and returns them in a sorted dictionary, and
        returns a second dictionary that will go into a Pandas df. """
    fitness_dict = {}
    generation_dict = {}
    for i in range(len(population)):
        child = assess_fitness(population[i])
        generation_dict[i] = child
        fitness_dict[i] = child[1]
    return sorted(fitness_dict.items(), key = operator.itemgetter(1), reverse = True), generation_dict


def selection(ranked_routes, percent_population_selected):
    """ Function takes in a dictionary of ranked routes and a percent of population to select, returns a list of the
        selected results. """
    selection_results = []
    df = pd.DataFrame(np.array(ranked_routes), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, percent_population_selected):
        selection_results.append(ranked_routes[i][0])
    for i in range(0, len(ranked_routes) - percent_population_selected):
        pick = 100 * random.random()
        for i in range(0, len(ranked_routes)):
            if pick <= df.iat[i, 3]:
                selection_results.append(ranked_routes[i][0])
                break
    return selection_results


def mating_pool(population, selection_results):
    """ Function creates a population for the mating pool based on the current generation and the selected results
        based upon fitness scores. """
    mating_pool_pop = []
    for i in range(0, len(selection_results)):
        index = selection_results[i]
        mating_pool_pop.append(population[index])
    return mating_pool_pop


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

def breedPopulation(mating_pool_pop, elite_size):
    """ Function returns a list of children who have undergone crossover events given parents. """
    children = []
    length = int((len(mating_pool_pop) - elite_size) / 2)
    pool = random.sample(mating_pool_pop, len(mating_pool_pop))

    for i in range(0, elite_size):
        children.append(mating_pool_pop[i])

    for i in range(0, length):
        crossover_children = crossover(pool[i], pool[len(mating_pool_pop) - i - 1])
        for child in crossover_children:
            children.append(child)
    return children

def mutation(child):
    """ Performs a mutation on a child and returns the mutated child. """
    for index_to_swap in range(len(child)):
        swap_with = int(random.random() * len(child))

        value_1 = child[index_to_swap]
        value_2 = child[swap_with]

        child[index_to_swap] = value_2
        child[swap_with] = value_1

    return child


def mutate_population(population):
    """ Performs mutations on each member of a population. """
    mutated_pop = []

    #mutating each individual in the pop
    for i in range(0, len(population)):
        mutated_ind = mutation(population[i])
        mutated_pop.append(mutated_ind)
    return mutated_pop


def next_generation(current_gen, elite_size):
    """ Calls for fitness scoring, selection criteria, mating pool generation, creation of children via crossover
        events, and mutations to generate a new population. """
    pop_ranked, fitness_dict = rank_routes(current_gen)
    selection_results = selection(pop_ranked, elite_size)
    mating_pool_pop = mating_pool(current_gen, selection_results)
    children = breedPopulation(mating_pool_pop, elite_size)
    next_generation = mutate_population(children)
    return next_generation


def genetic_algorithm(population, population_size, elite_size, generations):
    """ Full GA call with crossover, mutation, and fitness calculation steps. Creates progress file
        for the specified number of generations and a result file with the optimal path. """
    pop = initial_population(population_size, population)

    with open("Eden_Johnson_GA_TS_Info.txt", 'w') as f:
        iteration = 1

        for i in range(0, generations):
            pop = next_generation(pop, elite_size)
            pop_ranked, fitness_dict = rank_routes(pop)

            df = pd.DataFrame(fitness_dict)
            df.index = ["path", "fitness", "distance"]
            df = df.transpose()

            average_fitness_scores = df["distance"].mean()
            median_fitness_scores = df["distance"].median()
            std_fitness_scores = df["distance"].std()
            f.write(str(iteration) + ". " + "Population Size: " + str(population_size) + " for iteration " + str(iteration) + "\n")
            f.write("Average fitness scores " + str(average_fitness_scores) + "\n")
            f.write("Median fitness scores " + str(median_fitness_scores) + "\n")
            f.write("STD fitness scores " + str(std_fitness_scores) + "\n")
            f.write("Size of the selected subset of the population " + str(elite_size) + "\n\n")
            iteration += 1

    # Get the best route
    best_route_index = rank_routes(pop)[0][0][0]
    best_route = pop[best_route_index]

    # Write the best route into a text file
    with open("Eden_Johnson_GA_TS_Result.txt", 'w') as f:
        for i in best_route:
            f.write(str(i) + " " + str(index_dict[i]) + "\n")

genetic_algorithm(population=cities_index, population_size=100, elite_size=40, generations=50)


