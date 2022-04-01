#Universidad del Valle de Guatemala
#Inteligencia Artificial
#Integrantes:
# Bryann Alfaro
# Raul Jimenez
# Donaldo Garcia
# Oscar Saravia
#Tarea 4

from datetime import datetime
from funciones_tsp import *

import math
import sys
from matplotlib import pyplot as plt

ciudad_inicial = sys.argv[1]
ciudades = sys.argv[2]


# Abrir archivo de definicion de ciudades
ciudades = open(ciudades, "r")
numero_ciudades = ciudades.readline()

#print('Numero de ciudades: \n', numero_ciudades)

ciudades_list = {}
indice = 1
num_ciudad_inicial = ciudad_inicial
# Rellenando diccionario con ciudades y coordenadas
for ciudad in ciudades:
    ciudades_list['ciudad ' +
                  str(indice)] = {'x': float(ciudad.split()[0]), 'y': float(ciudad.split()[1])}
    try:
        if(float(ciudad_inicial) == indice):
            ciudad_inicial = ciudades_list['ciudad '+str(indice)]
    except:
        pass

    indice += 1

#print('Ciudad inicial: ', num_ciudad_inicial,' con coordenadas: ', ciudad_inicial)

#print('Lista de ciudades \n', ciudades_list)

#print('Distancia total: ', total_distance(ciudades_list))


n_population = 15

mutation_rate = 0.3

population_set1 = genesis(np.array(list(ciudades_list.keys())), n_population, int(numero_ciudades))
#print(population_set1)


fitnes_list = get_all_fitnes(population_set1,n_population,int(numero_ciudades),ciudades_list)
#print('fitness',fitnes_list)

prog_list = selection_prog(population_set1, fitnes_list)
#print('progenitor',prog_list[0][2])

new_population_set = mate_population(prog_list)
#print('new population set',new_population_set)

mutated_pop = mutate_population(new_population_set,int(numero_ciudades),mutation_rate)
#print('mutated population',mutated_pop)

best_solution = [-1,np.inf,np.array([])]
for i in range(5000):
    if i%100==0: print(i, fitnes_list.min(), fitnes_list.mean(), datetime.now().strftime("%d/%m/%y %H:%M"))
    fitnes_list = get_all_fitnes(mutated_pop,n_population,int(numero_ciudades),ciudades_list)

    #Saving the best solution
    if fitnes_list.min() < best_solution[1]:
        best_solution[0] = i
        best_solution[1] = fitnes_list.min()
        best_solution[2] = np.array(mutated_pop)[fitnes_list.min() == fitnes_list]

    progenitor_list = selection_prog(population_set1,fitnes_list)
    new_population_set = mate_population(progenitor_list)

    mutated_pop = mutate_population(new_population_set,float(numero_ciudades),mutation_rate)

print(best_solution)

#graphing best solution

f = 'ciudad ' + str(numero_ciudades)
fig = plt.figure()
ax2 = fig.add_subplot(122)
print(ciudades_list)
for first, second in zip(list(ciudades_list)[:-1], list(ciudades_list)[1:]):
    ax2.plot([ciudades_list[first]['x'], ciudades_list[second]['x']], [
             ciudades_list[first]['y'], ciudades_list[second]['y']], '-o')
#ax2.plot([(best_solution[0][2])['ciudad 1']['x'], (best_solution[0][2])[f.rstrip("\n")]['x']], [
#         (best_solution[0][2])['ciudad 1']['y'], best_solution[0][2][f.rstrip("\n")]['y']], '-o')

for c in list(ciudades_list):
    ax2.plot(ciudades_list[c]['x'], ciudades_list[c]['y'], 'bo')

plt.show()