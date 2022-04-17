# Universidad del Valle de Guatemala
# Inteligencia Artificial
# Integrantes:
# Bryann Alfaro
# Raul Jimenez
# Donaldo Garcia
# Oscar Saravia
# Tarea 4

import contextlib
from datetime import datetime
import pandas as pd
from funciones_tsp import *

import math
import sys
from matplotlib import pyplot as plt

ciudad_inicial = sys.argv[1]
ciudades = sys.argv[2]


# Abrir archivo de definicion de ciudades
ciudades = open(ciudades, "r")
numero_ciudades = ciudades.readline()

num_ciudad_inicial = ciudad_inicial
ciudades_list = {}
# Rellenando diccionario con ciudades y coordenadas
for indice, ciudad in enumerate(ciudades, start=1):
    ciudades_list['ciudad ' +
                  str(indice)] = {'x': float(ciudad.split()[0]), 'y': float(ciudad.split()[1])}
    with contextlib.suppress(Exception):
        if (float(ciudad_inicial) == indice):
            ciudad_inicial = ciudades_list[f'ciudad {str(indice)}']

# Datos para el algoritmo
n_population = 15
tasaMutacion = 0.3


firstPoblacionList = genesis(
    np.array(list(ciudades_list.keys())), n_population, int(numero_ciudades))


fitnes_list = get_all_fitnes(
    firstPoblacionList, n_population, int(numero_ciudades), ciudades_list)

progenitorList = selection_prog(firstPoblacionList, fitnes_list)

nuevaPoblacion = mate_population(progenitorList)

mutated_pop = mutate_population(
    nuevaPoblacion, int(numero_ciudades), tasaMutacion)

best_solution = [-1, np.inf, np.array([])]
print('Cargando...')
for i in range(5000):
    # if i % 100 == 0:
    #     print(i, fitnes_list.min(), fitnes_list.mean(),
    #           datetime.now().strftime("%d/%m/%y %H:%M"))
    fitnes_list = get_all_fitnes(
        mutated_pop, n_population, int(numero_ciudades), ciudades_list)

    # Saving the best solution
    if fitnes_list.min() < best_solution[1]:
        print('Cargando...')
        best_solution[0] = i
        best_solution[1] = fitnes_list.min()
        best_solution[2] = np.array(mutated_pop)[
            fitnes_list.min() == fitnes_list]

    progenitor_list = selection_prog(firstPoblacionList, fitnes_list)
    nuevaPoblacion = mate_population(progenitor_list)

    mutated_pop = mutate_population(
        nuevaPoblacion, float(numero_ciudades), tasaMutacion)

best_path = best_solution[2][0]
print('BEST SOLUTION:\n\tDistancia',
      best_solution[1])  # , '\n\tCamino', best_path)
first_city = list(ciudades_list.keys())[int(num_ciudad_inicial) - 1]
first_city_index = list(best_path).index(first_city)
show_best_path = list(best_path[first_city_index:])
show_best_path.extend(iter(list(best_path[:first_city_index])))
show_best_path.append(show_best_path[0])
print('\tCamino:', show_best_path)

# graphing best solution

# Draw the cities
fig = plt.figure(figsize=(10, 10))
for city in best_path:
    plt.plot(ciudades_list[city]['x'], ciudades_list[city]['y'], 'bo')
plt.title('TSP Problem')
plt.xlabel('Best path')
plt.show()

# Use plt to draw the conection of cities with the best path
fig = plt.figure(figsize=(10, 10))
cities = list(ciudades_list.keys())
plt.plot()
for pos in range(len(best_path)):
    city = best_path[pos]
    next_city = best_path[(pos + 1) % len(best_path)]
    pos_city = [ciudades_list[city]['x'], ciudades_list[next_city]['x']]
    next_pos_city = [ciudades_list[city]['y'], ciudades_list[next_city]['y']]
    plt.plot(pos_city, next_pos_city, 'r-')
plt.show()
