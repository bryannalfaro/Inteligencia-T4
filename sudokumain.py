# Codigo utilizado obtenido de https://github.com/mahdavipanah/sudoku_genetic_python
from math import sqrt
from random import shuffle, randint
from sudoku_utilities import *
import time


# CREANDO INSTANCIA DE LA CLASE UTILITIES
utils = Utilities()

#FUNCION PARA
def solve_sudoku(grd, pop_size=1000, rate=0.5, max_count=1000, mutation=0.05):
    N = int(sqrt(len(grd)))
    def empty(generator=None):
        return [[
                (None if generator is None else generator(i, j))
                for j in range(len(grd))
            ] for i in range(len(grd))
        ]

    def copy_deep(grid):
        return empty(lambda i, j: grid[i][j])

    grd = copy_deep(grd)

    def sub_gi(i, j, slf=True):
        for k in range(len(grd)):
            if k == j and not slf:
                continue

            yield (i, k)

    def fill_c():
        gtt = empty(lambda *args: [val for val in range(1, len(grd) + 1)])

        def pencil_mk(i, j):
            for x, y in sub_gi(i, j, slf=False):
                try:
                    gtt[x][y].remove(grd[i][j])
                except (ValueError, AttributeError) as e:
                    pass
            for x, y in utils.sri(grd, i, j, N, slf=False):
                try:
                    gtt[x][y].remove(grd[i][j])
                except (ValueError, AttributeError) as e:
                    pass
            for x, y in utils.same_col(grd, i, j, N, slf=False):
                try:
                    gtt[x][y].remove(grd[i][j])
                except (ValueError, AttributeError) as e:
                    pass

        for i in range(len(grd)):
            for j in range(len(grd)):
                if grd[i][j] is not None:
                    pencil_mk(i, j)

        while True:
            changes = False
            for i in range(len(grd)):
                for j in range(len(grd)):
                    if gtt[i][j] is None:
                        continue
                    if len(gtt[i][j]) == 0:
                        raise Exception('El puzzle no tiene solucion')
                    elif len(gtt[i][j]) == 1:
                        grd[i][j] = gtt[i][j][0]
                        pencil_mk(i, j)
                        gtt[i][j] = None
                        changes = True
            if not changes:
                break
        return grd

    def populate():
        cand = []
        for k in range(pop_size):
            candidate = empty()
            for i in range(len(grd)):
                shuff = [n for n in range(1, len(grd) + 1)]
                shuffle(shuff)
                for j in range(len(grd)):
                    if grd[i][j] is not None:
                        candidate[i][j] = grd[i][j]
                        shuff.remove(grd[i][j])
                for j in range(len(grd)):
                    if candidate[i][j] is None:
                        candidate[i][j] = shuff.pop()
            cand.append(candidate)
        return cand

    def fit(grid):
        reps = 0
        for a, b in utils.same_col(grd, 0, 0, N):
            row = list(utils.get_cells(grid, utils.sri(grd, a, b, N)))
            reps += len(row) - len(set(row))
        return reps

    def selections(cand):
        indexes_f = []
        for i in range(len(cand)):
            indexes_f.append(tuple([i, fit(cand[i])]))
        indexes_f.sort(key=lambda elem: elem[1])
        selected_part = indexes_f[0: int(len(indexes_f) * rate)]
        indexes = [e[0] for e in selected_part]
        return [cand[i] for i in indexes], selected_part[0][1]

    fill_c()
    population = populate()
    best_val = None
    for i in range(max_count):
        population, best_val = selections(population)
        if i == max_count - 1 or fit(population[0]) == 0:
            break
        shuffle(population)
        new_pop = []
        while True:
            sol1, sol2 = None, None
            try:
                sol1 = population.pop()
            except IndexError:
                break
            try:
                sol2 = population.pop()
            except IndexError:
                new_pop.append(sol2)
                break
            cross_point = randint(0, len(grd) - 2)
            temp_sub_grid = sol1[cross_point]
            sol1[cross_point] = sol2[cross_point + 1]
            sol2[cross_point + 1] = temp_sub_grid
            new_pop.append(sol1)
            new_pop.append(sol2)
        for candidate in new_pop[0:int(len(new_pop) * mutation)]:
            rndm_sg = randint(0, 8)
            exchanges = []
            for grid_ei in range(len(grd)):
                if grd[rndm_sg][grid_ei] is None:
                    exchanges.append(grid_ei)
            if len(exchanges) > 1:
                shuffle(exchanges)
                first_index = exchanges.pop()
                second_index = exchanges.pop()
                temporal = candidate[rndm_sg][first_index]
                candidate[rndm_sg][first_index] = candidate[rndm_sg][second_index]
                candidate[rndm_sg][second_index] = temporal
        population.extend(new_pop)
    return population[0], best_val


start_time = time.time()
with open('sudoku.txt', "r") as read_file:
    sudoku_content = read_file.read()
    all_lines = sudoku_content.split('\n')
    grd = [[] for i in range(len(all_lines))]
    square_rt_n = int(sqrt(len(all_lines)))
    for j in range(len(all_lines)):
        line_values = [(int(value) if value != '-' else None) for value in all_lines[j].split(' ')]
        for i in range(len(line_values)):
            grd[int(i / square_rt_n) + int(j / square_rt_n) * square_rt_n].append(line_values[i])
    solution, best_val = solve_sudoku(grd, pop_size=10000, rate=0.5, max_count=1000, mutation=0.05)
    answer = "Mejor valor encontrado: " + str(best_val) + '\n\n'
    for a, b in utils.same_col(solution, 0, 0, square_rt_n):
        row = list(utils.get_cells(solution, utils.sri(solution, a, b, square_rt_n)))
        answer += " ".join([str(elem) for elem in row]) + '\n'
    answer = answer
    print(answer[:-1])
print("--- %s seconds ---" % (time.time() - start_time))