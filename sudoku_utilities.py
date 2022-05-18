from math import sqrt
from random import shuffle, randint

# Codigo utilizado obtenido de https://github.com/mahdavipanah/sudoku_genetic_python

# SE DEFINE LA CLASE UTILITIES PARA PODER UTILIZARLO EN MAIN
class Utilities():
  def __init__(self):
    pass
  # SE DEFINE LA FUNCION PARA LAS COLUMNAS IGUALES
  def same_col(self, grd, i, j, N, slf=True):
      sub_grid_column = i % N
      cell_column = j % N
      # RECORRER EL SUBGRID
      for a in range(sub_grid_column, len(grd), N):
          for b in range(cell_column, len(grd), N):
              if (a, b) == (i, j) and not slf:
                  continue
              yield (a, b)

  # FUNCION PARA RECORRER EL ARREGLO
  def sri(self, grd, i, j, N, slf=True):
      sgr = int(i / N)
      cr = int(j / N)

      for a in range(sgr * N, sgr * N + N):
          for b in range(cr * N, cr * N + N):
              if (a, b) == (i, j) and not slf:
                  continue

              yield (a, b)

  # FUNCION PARA OBTENER LOS VALORES EN LAS CASILLAS CORRESPONDIENTES
  def get_cells(self, grid, indexes):
      for a, b in indexes:
          yield grid[a][b]

