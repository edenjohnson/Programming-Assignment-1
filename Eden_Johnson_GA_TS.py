import pandas as pd
import numpy as np
import random, operator

import ga_crossover
import ga_mutation
import tsp

#help(ga_crossover)
#help(ga_mutation)
#help(tsp)

distance_csv = pd.read_csv('TS_Distances_Between_Cities.csv', ',', index_col=0)
distance_df = distance_csv.dropna()


distance_matrix_path = 'TS_Distances_Between_Cities.csv'
generations = 50
percent_population_selected = 40
population_size = 100
progress_file_name = "Eden_Johnson_GA_TS_Info.txt"
results_file_name = "Eden_Johnson_GA_TS_Result.txt"

