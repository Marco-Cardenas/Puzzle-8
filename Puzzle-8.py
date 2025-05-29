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
Red = (255, 0, 0)
Blue = (100, 100, 255)

#Fuente
font_title = pygame.font.Font(None, 74)
font_button = pygame.font.Font(None, 30)
font_small = pygame.font.Font(None, 30)



#Dibujar Texto
def draw_text(text, font, color, surface, x, y):
  text_obj = font.render(text, True, color)
  text_rect = text_obj.get_rect()
  text_rect.center = (x, y)
  surface.blit(text_obj, text_rect)
  return text_rect

def draw_button(text, font, color, rect_color, surface, rect):
  pygame.draw.rect(surface, rect_color, rect)
  draw_text(text, font, color, surface, rect.centerx, rect.centery)

def draw_table(matrix = (1,2,3,4,5,6,7,8,0)):
  c00 = pygame.Rect(Width//2-150, 300, 100, 100)
  c01 = pygame.Rect(Width//2-50, 300, 100, 100)
  c02 = pygame.Rect(Width//2+50, 300, 100, 100)

  c10 = pygame.Rect(Width//2-150, 400, 100, 100)
  c11 = pygame.Rect(Width//2-50, 400, 100, 100)
  c12 = pygame.Rect(Width//2+50, 400, 100, 100)

  c20 = pygame.Rect(Width//2-150, 500, 100, 100)
  c21 = pygame.Rect(Width//2-50, 500,100, 100)
  c22 = pygame.Rect(Width//2+50, 500,100, 100)
  
  if matrix[0] != 0:
    draw_button(f"{matrix[0]}", font_small, White, Blue, Screen, c00)
  else: 
    draw_button(f"{matrix[0]}", font_small, Red, Red, Screen, c00)
  if matrix[1] != 0:
    draw_button(f"{matrix[1]}", font_small, White, Blue, Screen, c01)
  else: 
    draw_button(f"{matrix[1]}", font_small, Red, Red, Screen, c01)
  if matrix[2] != 0:
    draw_button(f"{matrix[2]}", font_small, White, Blue, Screen, c02)
  else: 
    draw_button(f"{matrix[2]}", font_small, Red, Red, Screen, c02)
  if matrix[3] != 0:
    draw_button(f"{matrix[3]}", font_small, White, Blue, Screen, c10)
  else: 
    draw_button(f"{matrix[3]}", font_small, Red, Red, Screen, c10)
  if matrix[4] != 0:
    draw_button(f"{matrix[4]}", font_small, White, Blue, Screen, c11)
  else: 
    draw_button(f"{matrix[4]}", font_small, Red, Red, Screen, c11)
  if matrix[5] != 0:
    draw_button(f"{matrix[5]}", font_small, White, Blue, Screen, c12)
  else: 
    draw_button(f"{matrix[5]}", font_small, Red, Red, Screen, c12)
  if matrix[6] != 0:
    draw_button(f"{matrix[6]}", font_small, White, Blue, Screen, c20)
  else: 
    draw_button(f"{matrix[6]}", font_small, Red, Red, Screen, c20)
  if matrix[7] != 0:
    draw_button(f"{matrix[7]}", font_small, White, Blue, Screen, c21)
  else: 
    draw_button(f"{matrix[7]}", font_small, Red, Red, Screen, c21)
  if matrix[8] != 0:
    draw_button(f"{matrix[8]}", font_small, White, Blue, Screen, c22)
  else: 
    draw_button(f"{matrix[8]}", font_small, Red, Red, Screen, c22)
  
  #draw_button(f"{matrix[1]}", font_small, White, Blue, Screen, c01)
  #draw_button(f"{matrix[2]}", font_small, White, Blue, Screen, c02)
  #draw_button(f"{matrix[3]}", font_small, White, Blue, Screen, c10)
  #draw_button(f"{matrix[4]}", font_small, White, Blue, Screen, c11)
  #draw_button(f"{matrix[5]}", font_small, White, Blue, Screen, c12)
  #draw_button(f"{matrix[6]}", font_small, White, Blue, Screen, c20)
  #draw_button(f"{matrix[7]}", font_small, White, Blue, Screen, c21)
  #draw_button(f"{matrix[8]}", font_small, White, Blue, Screen, c22)

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

tabla_inicial_auxB = None
tiempoAuxB = 0
visitedAuxB = 0
solucionB = None

def BFS(active_f):
  global solucionB
  global tabla_inicial_auxB
  global tiempoAuxB
  global visitedAuxB
  
  if active_f:
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
    solucionB = bfs8(tabla_inicial, tabla_final)
    time_end = time.time()
    tiempo_transcurrido = time_end - time_init
    tabla_inicial_auxB = tabla_inicial
    tiempoAuxB = tiempo_transcurrido
    visitedAuxB = visitados
    if solucionB:
      print("Solucion encontrada\n")
      for i, sol in enumerate(solucionB):
        print(f"Paso: {i}")
        for j in range(3):
          print(sol[j*3:j*3+3])
        
        print("=" * 10)
      
      print(f"Cantidad de movimientos usados: {len(solucionB) - 1}")
      
      print(f"Cantidad de tiempo requerido: {tiempo_transcurrido:.4f}s")

      print(f"Cantidad de nodos explorados: {len(visitados)}")

      
    else:
      print("No se ha encontrado solucion para la siguiente tabla inicial")
      print(f"Cantidad de tiempo requerido: {tiempo_transcurrido:.4f}s")
      print(f"Cantidad de nodos explorados: {len(visitados)}")
      for i in range(3):
        print(tabla_inicial[i*3:i*3+3])
  
  #draw_text("BFS", font_title, Black, Screen, Width//2, 100)

  if solucionB != None: 
    for i, sol in enumerate(solucionB):
      Screen.fill(White)
      draw_text(f"Paso {i}", font_title, Black, Screen, Width//2, 100)
      draw_text(f"Tiempo requerido: {tiempoAuxB:.4f}s", font_small, Black, Screen, Width//2, 130)
      draw_text(f"Cantidad de movimientos usados: {len(solucionB) - 1}", font_small, Black, Screen, Width//2, 160)
      draw_text(f"Cantidad de nodos explorados: {len(visitedAuxB)}", font_small, Black, Screen, Width//2, 190)
      
      draw_table(sol)
      pygame.display.flip()
      pygame.time.delay(1000)


  else:
    draw_text(f"No se encontro solucion para la tabla", font_small, Black, Screen, Width//2, 100)
    draw_text(f"Tiempo requerido: {tiempoAuxB:.4f}s", font_small, Black, Screen, Width//2, 130)
    draw_text(f"Cantidad de nodos explorados: {len(visitedAuxB)}", font_small, Black, Screen, Width//2, 190)
    draw_table(tabla_inicial_auxB)
    pygame.display.flip()  
    pygame.time.delay(6000)
    pygame.quit()
    exit()

  for ev in pygame.event.get():
    if ev.type == pygame.QUIT:
      pygame.quit()
      exit()




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

tabla_inicial_auxA = None
tiempoAuxA = 0
visitedAuxA = 0
solucionA = None
def A_ast(active_f):
  global solucionA
  global tabla_inicial_auxA
  global tiempoAuxA
  global visitedAuxA
  if active_f:
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
    tabla_inicial_auxA = tabla_inicial
    time_init = time.time()
    solucionA = A_ast.solve(tabla_inicial)
    time_end = time.time()
    tiempo_transcurrido = time_end - time_init
    tiempoAuxA = tiempo_transcurrido
    visitedAuxA = A_ast.get_visited()
    if solucionA:
      for i, sol in enumerate(solucionA):
        print(f"\nPaso {i}:")
        A_ast.print_tabla(sol)
        print("=" * 10)
      
      print(f"\nCantidad de movimientos usados: {len(solucionA) - 1}")
      
      print(f"Cantidad de tiempo requerido: {tiempo_transcurrido:.4f}s")

      print(f"Cantidad de nodos explorados: {len(A_ast.get_visited())}")

    else:
      print("\nNo se ha encontrado solucion")
    
      print(f"Cantidad de tiempo requerido: {tiempo_transcurrido:.4f}s")

      print(f"Cantidad de nodos explorados: {len(A_ast.get_visited())}")
  
  #draw_text("A*", font_title, Black, Screen, Width//2, 100)

  if solucionA != None: 
    for i, sol in enumerate(solucionA):
      Screen.fill(White)
      draw_text(f"Paso {i}", font_title, Black, Screen, Width//2, 100)
      draw_text(f"Tiempo requerido: {tiempoAuxA:.4f}s", font_small, Black, Screen, Width//2, 130)
      draw_text(f"Cantidad de movimientos usados: {len(solucionA) - 1}", font_small, Black, Screen, Width//2, 160)
      draw_text(f"Cantidad de nodos explorados: {len(visitedAuxA)}", font_small, Black, Screen, Width//2, 190)
      
      draw_table(sol)
      pygame.display.flip()
      pygame.time.delay(1000)


  else:
    draw_text(f"No se encontro solucion para la tabla", font_small, Black, Screen, Width//2, 100)
    draw_text(f"Tiempo requerido: {tiempoAuxA:.4f}s", font_small, Black, Screen, Width//2, 130)
    draw_text(f"Cantidad de nodos explorados: {len(visitedAuxA)}", font_small, Black, Screen, Width//2, 190)
    draw_table(tabla_inicial_auxA)
    pygame.display.flip()  
    pygame.time.delay(6000)
    pygame.quit()
    exit()

  for ev in pygame.event.get():
    if ev.type == pygame.QUIT:
      pygame.quit()
      exit()  

def compare_algorithms(active_f):
  draw_text("BFS vs A*", font_title, Black, Screen, Width//2, 100)

 # draw_table()

  for ev in pygame.event.get():
    if ev.type == pygame.QUIT:
      pygame.quit()
      exit()
  
def Salir():
  pygame.quit()
  exit()




active_func = True
menu, op1, op2, op3, op4 = 0, 1, 2, 3, 4
current_state = menu

def menu_principal():
  global current_state

  draw_text("Puzzle 8", font_title, Black, Screen, Width//2, 100)
  opa = pygame.Rect(Width//2-150, 200, 300, 60)
  opb = pygame.Rect(Width//2-150, 280, 300, 60)
  #opc = pygame.Rect(Width//2-150, 360, 300, 60)
  opd = pygame.Rect(Width//2-150, 360, 300, 60)

  draw_button("BFS", font_small, White, Blue, Screen, opa)
  draw_button("A*", font_small, White, Blue, Screen, opb)
  #draw_button("BFS vs A*", font_small, White, Blue, Screen, opc)
  draw_button("Salir", font_small, White, Blue, Screen, opd)

  for ev in pygame.event.get():
    if ev.type == pygame.QUIT:
      pygame.quit()
      exit()
    if ev.type == pygame.MOUSEBUTTONDOWN:
      if opa.collidepoint(ev.pos):
        current_state = op1
      elif opb.collidepoint(ev.pos):
        current_state = op2
      #elif opc.collidepoint(ev.pos):
       # current_state = op3
      elif opd.collidepoint(ev.pos):
        current_state = op4

click = False
running = True
while running:
  Screen.fill(White)

  if current_state == menu:
    menu_principal()
  elif current_state == op1:
    BFS(active_func)
    pygame.quit()
    exit()
    active_func = False
  elif current_state == op2:
    A_ast(active_func)
    pygame.quit()
    exit()
    active_func = False
  elif current_state == op3:
    compare_algorithms(active_func)
    active_func = False
  elif current_state == op4:
    Salir()
  
  pygame.display.flip()
  
