import pygame
import sys

# --- Configuración ---
ANCHO = 800
ALTO = 600
TITULO = "Captura la Bandera"

# Colores
BLANCO = (255, 255, 255)
ROJO = (200, 50, 50)
AZUL = (50, 50, 200)
VERDE = (50, 200, 50) # Color de la bandera
GRIS = (200, 200, 200)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(TITULO)
reloj = pygame.time.Clock()

# --- Definición de Zonas ---
# Zona de anotación Roja (Toda la franja izquierda)
BASE_ROJA = pygame.Rect(0, 0, 100, ALTO)
# Zona de anotación Azul (Toda la franja derecha)
BASE_AZUL = pygame.Rect(ANCHO - 100, 0, 100, ALTO)

# --- Clases Simples ---

class Jugador:
    def __init__(self, x, y, color, controles):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.controles = controles # Diccionario de teclas
        self.velocidad = 6
        self.puntos = 0

    def mover(self):
        teclas = pygame.key.get_pressed()
        
        if teclas[self.controles['arriba']] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[self.controles['abajo']] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad
        if teclas[self.controles['izq']] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[self.controles['der']] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

    def dibujar(self):
        pygame.draw.rect(pantalla, self.color, self.rect)
        # Borde negro para que se vea mejor
        pygame.draw.rect(pantalla, (0,0,0), self.rect, 2)

class Bandera:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.center = (ANCHO // 2, ALTO // 2) # EN EL MEDIO
        self.portador = None # 'rojo', 'azul' o None

    def reiniciar(self):
        self.portador = None
        self.rect.center = (ANCHO // 2, ALTO // 2)

    def actualizar(self, jugador_rojo, jugador_azul):
        # 1. Si nadie la tiene, comprobar si alguien la toca
        if self.portador is None:
            if self.rect.colliderect(jugador_rojo.rect):
                self.portador = jugador_rojo
            elif self.rect.colliderect(jugador_azul.rect):
                self.portador = jugador_azul
        
        # 2. Si alguien la tiene, la bandera sigue al jugador
        else:
            self.rect.center = self.portador.rect.center

    def dibujar(self):
        pygame.draw.rect(pantalla, VERDE, self.rect)
        pygame.draw.rect(pantalla, (0,0,0), self.rect, 2)

# --- Crear Objetos ---

# Controles
teclas_rojo = {'arriba': pygame.K_w, 'abajo': pygame.K_s, 'izq': pygame.K_a, 'der': pygame.K_d}
teclas_azul = {'arriba': pygame.K_UP, 'abajo': pygame.K_DOWN, 'izq': pygame.K_LEFT, 'der': pygame.K_RIGHT}

# Jugadores (Empiezan pegados a sus paredes)
j_rojo = Jugador(20, ALTO//2 - 20, ROJO, teclas_rojo)
j_azul = Jugador(ANCHO - 60, ALTO//2 - 20, AZUL, teclas_azul)

bandera = Bandera()

# --- Bucle Principal ---
ejecutando = True
while ejecutando:
    # 1. Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # 2. Lógica
    j_rojo.mover()
    j_azul.mover()
    
    # Lógica de la bandera (recoger y seguir)
    bandera.actualizar(j_rojo, j_azul)

    # --- Lógica de Puntos ---
    
    # Si la tiene el ROJO y toca la BASE ROJA (Izquierda)
    if bandera.portador == j_rojo and j_rojo.rect.colliderect(BASE_ROJA):
        j_rojo.puntos += 1
        print(f"¡Punto Rojo! Marcador - Rojo: {j_rojo.puntos} | Azul: {j_azul.puntos}")
        bandera.reiniciar() # La bandera vuelve al centro
        # Opcional: Devolver jugadores a inicio
        j_rojo.rect.topleft = (20, ALTO//2 - 20)
        j_azul.rect.topleft = (ANCHO - 60, ALTO//2 - 20)

    # Si la tiene el AZUL y toca la BASE AZUL (Derecha)
    elif bandera.portador == j_azul and j_azul.rect.colliderect(BASE_AZUL):
        j_azul.puntos += 1
        print(f"¡Punto Azul! Marcador - Rojo: {j_rojo.puntos} | Azul: {j_azul.puntos}")
        bandera.reiniciar()
        # Opcional: Devolver jugadores a inicio
        j_rojo.rect.topleft = (20, ALTO//2 - 20)
        j_azul.rect.topleft = (ANCHO - 60, ALTO//2 - 20)

    # 3. Dibujar
    pantalla.fill(BLANCO)
    
    # Dibujar bases (zonas gris claro)
    pygame.draw.rect(pantalla, GRIS, BASE_ROJA)   # Zona Izquierda
    pygame.draw.rect(pantalla, GRIS, BASE_AZUL)   # Zona Derecha
    
    # Linea central decorativa
    pygame.draw.line(pantalla, (220, 220, 220), (ANCHO//2, 0), (ANCHO//2, ALTO), 2)

    # Dibujar entidades
    j_rojo.dibujar()
    j_azul.dibujar()
    bandera.dibujar()

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()