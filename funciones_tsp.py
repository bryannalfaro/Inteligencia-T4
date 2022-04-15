import contextlib
import math
import numpy as np


def distance_points(a, b):
    return math.sqrt((a['x']-b['x'])**2 + (a['y']-b['y'])**2)


def total_distance(ciudades_list):
    total = 0
    longitud = len(ciudades_list)
    for i in range(len(ciudades_list)):
        with contextlib.suppress(Exception):
            total += distance_points(
                ciudades_list[f'ciudad {str(i+1)}'],
                ciudades_list[f'ciudad {str(i + 2)}'],
            )

    total += distance_points(ciudades_list['ciudad 1'],
                             ciudades_list['ciudad '+str(longitud).rstrip("\n")])
    return total


def genesis(city_list, n_population, NumCities):

    population_set = [city_list[np.random.choice(
        list(range(NumCities)), NumCities, replace=False)] for _ in range(n_population)]

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

    progenitor_a = population[progenitor_a]
    progenitor_b = population[progenitor_b]

    return np.array([progenitor_a, progenitor_b])


def mate_progenitors(prog_a, prog_b):
    offspring = prog_a[:5]

    for city in prog_b:

        if city not in offspring:
            offspring = np.concatenate((offspring, [city]))

    return offspring


def mate_population(original_list):
    newPopulation = []
    for i in range(original_list.shape[1]):
        prog_a, prog_b = original_list[0][i], original_list[1][i]
        offspring = mate_progenitors(prog_a, prog_b)
        newPopulation.append(offspring)

    return newPopulation


def mutate_offspring(offspring, NumCities, mutation_rate):
    for _ in range(int(NumCities*mutation_rate)):
        a = np.random.randint(0, NumCities)
        b = np.random.randint(0, NumCities)

        offspring[a], offspring[b] = offspring[b], offspring[a]

    return offspring


def mutate_population(newPopulation, NumCities, mutation_rate):
    return [mutate_offspring(item, NumCities, mutation_rate) for item in newPopulation]
