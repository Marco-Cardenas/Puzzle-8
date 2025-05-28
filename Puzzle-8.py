import pygame
import collections
import time
import random
import heapq


#iniciamos pygame
pygame.init()

#definimos tamanio de la ventana y el titulo
Width, Height = 600, 700
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("PUZZLE 8")

#Definimos algunos colores a usar en formato rgb
White = (255, 255, 255)
Black = (0, 0, 0)
Gray = (200, 200, 200)
Blue = (100, 100, 255)

#Fuente
font_title = pygame.font.Font(None, 74)
font_button = pygame.font.Font(None, 30)

#Dibujar Texto
def draw_text(text, font, color, surface, x, y):
  text_obj = font.render(text, True, color)
  text_rect = text_obj.get_rect()
  text_rect.center = (x, y)
  surface.blit(text_obj, text_rect)

#Crear botones
class Button:
  def __init__(self, x, y, width, height, text, action=None):
    self.rect = pygame.Rect(x, y, width, height)
    self.text = text
    self.action = action
    self.color = Gray
  
  def draw(self, surface):
    pygame.draw.rect(surface, self.color, self.rect)
    draw_text(self.text, font_button, Black, surface, self.rect.centerx, self.rect.centery)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        if self.action:
          self.action()
    
    #Cambiar el color del texto cuando pasamos el mouse sobre el boton
    if event.type == pygame.MOUSEMOTION:
      if self.rect.collidepoint(event.pos):
        self.color = Blue
      else:
        self.color = Gray

#Funcion para generar los tableros iniciales
def generate_initial_array():
  #creamos una lista del 0 al 8
  nums = list(range(9))

  #randomizamos las posiciones dentro del arreglo
  random.shuffle(nums)

  return tuple(nums)

visitados = {}
def bfs8(tabla_i, tabla_f):
  movimientos = { 'arriba':(-1, 0), 'abajo':(1, 0), 'izquierda':(0, -1), 'derecha':(0, 1) } #movimientos posibles
  cola = collections.deque([(tabla_i, [tabla_i])]) #la cola de los nodos a explorar
  global visitados
  visitados = {tabla_i} #nodos ya explorados

  while cola:
    tabla_actual, camino_actual = cola.popleft()

    #Si la tabla actual es igual que la tabla final entonces ya estuvo
    if tabla_actual == tabla_f:
      return camino_actual
    
    index_0 = tabla_actual.index(0) #Buscamos el indice del 0 en la tupla
    f0, c0 = divmod(index_0, 3) #llevamos nuestro indice de 1D a 2D

    for direccion, (dirR, dirC) in movimientos.items():
      newF, newC = f0 + dirR, c0 + dirC
      
      #verificamos si el moivmiento es valido en el estado actual
      if 0 <= newF <= 2 and 0 <= newC <= 2:
        new_index_0 = newF * 3 + newC

        #como las tuplas son inmutables, esto lo uso para poder modificar a un nuevo tablero
        lista_tabla = list(tabla_actual)

        #intercambiar el 0 (el espacio) con la ficha a mover (nuestro nuevo estado)
        lista_tabla[index_0], lista_tabla[new_index_0] = lista_tabla[new_index_0], lista_tabla[index_0]

        nueva_tabla = tuple(lista_tabla)

        if nueva_tabla not in visitados:
          visitados.add(nueva_tabla)
          cola.append((nueva_tabla, camino_actual + [nueva_tabla]))

  #Ya revisamos todo los estados y no se consiguio respuesta
  return None

def BFS():
  tabla_inicial = generate_initial_array()
  tabla_final = (
    1, 2, 3,
    8, 0, 4,
    7, 6, 5
  )
  while True:
    if tabla_inicial == tabla_final:
      tabla_inicial = generate_initial_array()
    else:
      break

  time_init = time.time()
  solucion = bfs8(tabla_inicial, tabla_final)
  time_end = time.time()
  tiempo_transcurrido = time_end - time_init

  if solucion:
    print("Solucion encontrada\n")
    for i, sol in enumerate(solucion):
      print(f"Paso: {i}")
      for j in range(3):
        print(sol[j*3:j*3+3])
      
      print("=" * 10)
    
    print(f"Cantidad de movimientos usados: {len(solucion) - 1}")
    
    print(f"Cantidad de tiempo requerido: {tiempo_transcurrido:.4f}s")

    print(f"Cantidad de nodos explorados: {len(visitados)}")

    
  else:
    print("No se ha encontrado solucion para la siguiente tabla inicial")
    print(f"Cantidad de tiempo requerido: {tiempo_transcurrido:.4f}s")
    print(f"Cantidad de nodos explorados: {len(visitados)}")
    for i in range(3):
      print(tabla_inicial[i*3:i*3+3])



class Node:
  def __init__(self, state, parent=None, gx=0, hx=0):
    self.state = state
    self.parent = parent
    self.gx = gx
    self.hx = hx
    self.fx = gx + hx
  
  def __lt__(self, other):
    return self.fx < other.fx

  def __eq__(self, other):
    return self.state == other.state
  
  def __hash__(self):
    return hash(self.state)
  
class Puzzle8:
  def __init__(self, state_f):
    self.state_f = state_f
    self.visitados = set()

  def get_coords(self, index): #convierte indice 1D a 2D
    return index//3, index%3

  def get_index(self, row, col): #de indice 2D a 1D
    return row * 3 + col
  
  def manhatthan(self, state):
    distance = 0
    for i in range(9):
      if state[i] == 0: #ignoramos el 0
        continue
      
      actual_r, actual_c = self.get_coords(i)

      #Buscamos donde deberia encontrarse el numero en el tablero meta
      index_t = self.state_f.index(state[i])
      row_t, col_t = self.get_coords(index_t)

      distance += abs(actual_r - row_t) + abs(actual_c - col_t)
    
    return distance

  def get_neighbors(self, state):
    neighbors = []
    index_0 = state.index(0)
    row0, col0 = self.get_coords(index_0)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dirR, dirC in moves:
      newR, newC = row0 + dirR, col0 + dirC

      if 0 <= newR <= 2 and 0 <= newC <= 2:
        new_index_0 = self.get_index(newR, newC)

        lista_tabla = list(state)
        lista_tabla[index_0], lista_tabla[new_index_0] = lista_tabla[new_index_0], lista_tabla[index_0]
        neighbors.append(tuple(lista_tabla))
    
    return neighbors

  def solve(self, state_i):
    initial_state = tuple(state_i)
    h_func = self.manhatthan

    if initial_state == self.state_f:
      return self.reconstruir_nodos(Node(estado_inicial))

    priority_list = []
    heapq.heappush(priority_list, Node(initial_state, gx=0, hx=h_func(initial_state)))
    
    camino = {}

    g_score = {initial_state: 0}

    while priority_list:
      actual_node = heapq.heappop(priority_list)
      actual_state = actual_node.state

      if actual_state == self.state_f:
        return self.reconstruir_nodos(actual_node)

      self.visitados.add(actual_state)
      for neighbor_state in self.get_neighbors(actual_state):
        if neighbor_state in self.visitados:
          continue
        
        g_score_t = actual_node.gx + 1

        if neighbor_state not in g_score or g_score_t < g_score[neighbor_state]:
          g_score[neighbor_state] = g_score_t
          h_score = h_func(neighbor_state)
          neighbor_node = Node(neighbor_state, parent=actual_node, gx=g_score_t, hx=h_score)
          heapq.heappush(priority_list, neighbor_node)

    return None

  def reconstruir_nodos(self, actual_node):
    camino = []
    while actual_node:
      camino.append(actual_node.state)
      actual_node = actual_node.parent
    return camino[::-1]

  def print_tabla(self, tabla):
    for i in range(0, 9, 3):
      print(tabla[i], tabla[i+1], tabla[i+2])
  
  def get_visited(self):
    return self.visitados
  
def A_ast():
  tabla_inicial = generate_initial_array()
  tabla_final = (
    1, 2, 3,
    8, 0, 4,
    7, 6, 5
  )

  while True:
    if tabla_inicial == tabla_final:
      tabla_inicial = generate_initial_array()
    else:
      break

  A_ast = Puzzle8(tabla_final)

  time_init = time.time()
  solucion = A_ast.solve(tabla_inicial)
  time_end = time.time()
  tiempo_transcurrido = time_end - time_init

  if solucion:
    for i, sol in enumerate(solucion):
      print(f"\nPaso {i}:")
      A_ast.print_tabla(sol)
      print("=" * 10)
    
    print(f"\nCantidad de movimientos usados: {len(solucion) - 1}")
    
    print(f"Cantidad de tiempo requerido: {tiempo_transcurrido:.4f}s")

    print(f"Cantidad de nodos explorados: {len(A_ast.get_visited())}")

  else:
    print("\nNo se ha encontrado solucion")
  
    print(f"Cantidad de tiempo requerido: {tiempo_transcurrido:.4f}s")

    print(f"Cantidad de nodos explorados: {len(A_ast.get_visited())}")

def compare_algorithms():
  print("BFS vs A*")

def Salir():
  print("Salir")
  pygame.quit()
  exit()

button_width = 250
button_height = 70
button_spacing = 30

button_start_y = Height//2 - (button_height * 1.5 + button_spacing) #Centramos los botones

button1 = Button(Width//2 - button_width//2, button_start_y, button_width, button_height, "Resolver por BFS", BFS)
button2 = Button(Width//2 - button_width//2, button_start_y + button_height + button_spacing, button_width, button_height, "Resolver por A*", A_ast)
button3 = Button(Width//2 - button_width//2, button_start_y + (button_height + button_spacing) * 2, button_width, button_height, "BFS vs A*", compare_algorithms)
button4 = Button(Width//2 - button_width//2, button_start_y + (button_height + button_spacing) * 3, button_width, button_height, "Salir", Salir)

buttons = [button1, button2, button3, button4]

#Bucle del pygame
game_state = True
while game_state:

  #Detectamos los eventos
  for ev in pygame.event.get():
    if ev.type == pygame.QUIT:
      game_state = False
    
    for button in buttons:
      button.handle_event(ev)
  
  #Dibujar en pantalla
  Screen.fill(White)

  #Dibujar titulo
  draw_text("PUZZLE 8", font_title, Blue, Screen, Width//2, Height//4)

  #Dibujar botones
  for button in buttons:
    button.draw(Screen)
  
  pygame.display.flip()





#cerrar pygame
pygame.quit()