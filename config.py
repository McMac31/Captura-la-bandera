import pygame
import random


# Configuración de Pantalla
ANCHO = 800
ALTO = 600
TITULO = "Captura la Bandera"
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
def generar_obstaculos():
    lista = []
    # Zona de la bandera para evitar colocar muros encima
    zona_bandera = pygame.Rect(ANCHO//2 - 50, ALTO//2 - 50, 100, 100)
    
    # Creamos 10 obstáculos aleatorios
    for _ in range(10): 
        intentos = 0
        while intentos < 50: # Evitar bucle infinito
            w = random.randint(40, 150) # Ancho aleatorio
            h = random.randint(40, 150) # Alto aleatorio
            x = random.randint(0, ANCHO - w)
            y = random.randint(0, ALTO - h)
            muro = pygame.Rect(x, y, w, h)
            
            # NO chocar con la bandera
            if muro.colliderect(zona_bandera):
                intentos += 1
                continue
                
            # NO chocar con ninguna base
            if (muro.colliderect(BASE_ROJA) or 
                muro.colliderect(BASE_AZUL) or 
                muro.colliderect(BASE_AMARILLA) or 
                muro.colliderect(BASE_VERDE)):
                intentos += 1
                continue
                
            # Si pasa las pruebas, lo añadimos
            lista.append(muro)
            break
    return lista

# Generamos la lista al iniciar
OBSTACULOS = generar_obstaculos()

# Controles Jugador local
TECLAS_LOCAL = {'arriba': pygame.K_w, 'abajo': pygame.K_s, 'izq': pygame.K_a, 'der': pygame.K_d}

#Configuracion de red
SERVIDOR_IP = "192.168.24.219"
PUERTO=8000
DIRECCION_SERVIDOR = (SERVIDOR_IP, PUERTO)