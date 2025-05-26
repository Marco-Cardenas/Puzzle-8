import pygame

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

def BFS():
  print("Usando BFS")

def A_ast():
  print("Usando A_ast")

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