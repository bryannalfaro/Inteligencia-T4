import math
import numpy as np


def distance_points(a, b):
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


def genesis(city_list, n_population, n_cities):

    population_set = []
    for i in range(n_population):
        # Randomly generating a new solution
        population_set.append(city_list[np.random.choice(
            list(range(n_cities)), n_cities, replace=False)])
    return np.array(population_set)


def fitness_eval(city_list, numero_ciudades, ciudades_list):
    total = 0
    for i in range(numero_ciudades-1):
        a = ciudades_list[city_list[i]]
        b = ciudades_list[city_list[i+1]]

        total += distance_points(a, b)
    return total


def get_all_fitnes(population_set, n_population, numero_ciudades, ciudades_list):
    fitnes_list = np.zeros(n_population)

    # Looping over all solutions computing the fitness for each solution
    for i in range(n_population):
        fitnes_list[i] = fitness_eval(
            population_set[i], numero_ciudades, ciudades_list)

    return fitnes_list


def selection_prog(population, fitnes_list):
    total = fitnes_list.sum()
    prob_list = fitnes_list / total
    progenitor_a = np.random.choice(list(range(len(population))), len(
        population), p=prob_list, replace=True)
    progenitor_b = np.random.choice(list(range(len(population))), len(
        population), p=prob_list, replace=True)

    # print(progenitor_a,progenitor_b)

    progenitor_a = population[progenitor_a]
    progenitor_b = population[progenitor_b]

    # print(progenitor_a,progenitor_b)

    return np.array([progenitor_a, progenitor_b])


def mate_progenitors(prog_a, prog_b):
    offspring = prog_a[0:5]

    for city in prog_b:

        if not city in offspring:
            offspring = np.concatenate((offspring, [city]))

    return offspring


def mate_population(progenitor_list):
    new_population_set = []
    for i in range(progenitor_list.shape[1]):
        prog_a, prog_b = progenitor_list[0][i], progenitor_list[1][i]
        offspring = mate_progenitors(prog_a, prog_b)
        new_population_set.append(offspring)

    return new_population_set


def mutate_offspring(offspring, n_cities, mutation_rate):
    for q in range(int(n_cities*mutation_rate)):
        a = np.random.randint(0, n_cities)
        b = np.random.randint(0, n_cities)

        offspring[a], offspring[b] = offspring[b], offspring[a]

    return offspring


def mutate_population(new_population_set, n_cities, mutation_rate):
    mutated_pop = []
    for offspring in new_population_set:
        mutated_pop.append(mutate_offspring(
            offspring, n_cities, mutation_rate))
    return mutated_pop
