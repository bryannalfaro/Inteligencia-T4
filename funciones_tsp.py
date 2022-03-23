import math
import numpy as np


def distance_points(a, b):
    print(a,b)
    return math.sqrt((a['x']-b['x'])**2 + (a['y']-b['y'])**2)


def total_distance(ciudades_list):
    total = 0
    longitud = len(ciudades_list)
    for i in range(len(ciudades_list)):
        try:
            total += distance_points(
                ciudades_list[f'ciudad {str(i+1)}'],
                ciudades_list[f'ciudad {str(i + 2)}'],
            )

        except:
            pass

    total += distance_points(ciudades_list['ciudad 1'],
                             ciudades_list['ciudad '+str(longitud).rstrip("\n")])
    return total

def genesis(city_list, n_population,n_cities):

    population_set = []
    for i in range(n_population):
        #Randomly generating a new solution
        population_set.append(city_list[np.random.choice(list(range(n_cities)), n_cities, replace=False)])
    return np.array(population_set)



def fitness_eval(city_list,numero_ciudades):
    total = 0
    for i in range(numero_ciudades-1):
        a = city_list[i]
        b = city_list[i+1]
        total += distance_points(a,b)
    return total

def get_all_fitnes(population_set,n_population,numero_ciudades,ciudades_list):
    fitnes_list = np.zeros(n_population)

    #Looping over all solutions computing the fitness for each solution
    for i in  range(n_population):
        fitnes_list[i] = fitness_eval(population_set[i],numero_ciudades,ciudades_list)

    return fitnes_list

