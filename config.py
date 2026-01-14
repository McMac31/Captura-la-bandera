import pygame


# Configuración de Pantalla
ANCHO = 800
ALTO = 600
TITULO = "Captura la Bandera - 4 Jugadores"
FPS = 60

#  Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
VERDE_BANDERA = (50, 200, 50) # Diferenciamos el verde de la bandera

# Colores de Jugadores
ROJO = (200, 50, 50)
AZUL = (50, 50, 200)
AMARILLO = (220, 220, 50)
VERDE = (50, 180, 50)

# Colores de Bases
COLOR_BASE_ROJA = (255, 150, 150)
COLOR_BASE_AZUL = (150, 150, 255)
COLOR_BASE_AMARILLA = (255, 255, 150)
COLOR_BASE_VERDE = (150, 230, 150)

# Definición de Bases
TAMANO_BASE = 80 # Bases cuadradas de 80x80
BASE_ROJA = pygame.Rect(0, 0, TAMANO_BASE, TAMANO_BASE)                    # Esquina Superior Izquierda
BASE_AZUL = pygame.Rect(ANCHO - TAMANO_BASE, 0, TAMANO_BASE, TAMANO_BASE)  # Esquina Superior Derecha
BASE_AMARILLA= pygame.Rect(0, ALTO - TAMANO_BASE, TAMANO_BASE, TAMANO_BASE) # Esquina Inferior Izquierda
BASE_VERDE = pygame.Rect(ANCHO - TAMANO_BASE, ALTO - TAMANO_BASE, TAMANO_BASE, TAMANO_BASE) # Esquina Inferior Derecha

# Obstáculos 
OBSTACULOS = [
    pygame.Rect(200, 100, 20, 400),   # Muro vertical izquierdo
    pygame.Rect(580, 100, 20, 400),   # Muro vertical derecho
    pygame.Rect(100, 400, 80, 20),    # Obstáculo extra izquierda
    pygame.Rect(620, 200, 80, 20)     # Obstáculo extra derecha
]

# Controles Jugador local
TECLAS_LOCAL = {'arriba': pygame.K_w, 'abajo': pygame.K_s, 'izq': pygame.K_a, 'der': pygame.K_d}

#Configuracion de red

SERVIDOR_IP = "127.0.0.1" #Localhost
PUERTO=8000
DIRECCION_SERVIDOR = (SERVIDOR_IP, PUERTO)