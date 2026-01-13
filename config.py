import pygame

#  Configuración de Pantalla
ANCHO = 800
ALTO = 600
TITULO = "Captura la Bandera"
FPS = 60

# Colores 
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 50, 50)
AZUL = (50, 50, 200)
VERDE = (50, 200, 50)
GRIS = (200, 200, 200)
COLOR_BASEROJA = (254, 120, 118)
COLOR_BASEAZUL = (114, 106, 235)

# Rectángulos
# Creamos los rectángulos aquí para usarlos en el juego
BASE_ROJA_RECT = pygame.Rect(0, 0, 100, ALTO)
BASE_AZUL_RECT = pygame.Rect(ANCHO - 100, 0, 100, ALTO)

# Controles 
TECLAS_ROJO = {'arriba': pygame.K_w, 'abajo': pygame.K_s, 'izq': pygame.K_a, 'der': pygame.K_d}
TECLAS_AZUL = {'arriba': pygame.K_UP, 'abajo': pygame.K_DOWN, 'izq': pygame.K_LEFT, 'der': pygame.K_RIGHT}