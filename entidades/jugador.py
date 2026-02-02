import pygame
from config import *

#Clase Jugador
class Jugador:
    # Inicializamos clase jugador y atributos
    def __init__(self, x, y, color, id_jugador, NombreJugador, EmailJugador, es_local=False):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.velocidad = 5
        self.puntos = 0 # Puntos del jugador
        self.inicio_x = x
        self.inicio_y = y
        self.NombreJugador=NombreJugador
        self.EmailJugador=EmailJugador
        # Atributos para red
        self.id = id_jugador # Identificador único del jugador
        self.es_local = es_local  # True si soy yo, False si es otro cliente
        self.controles = None     # Se asignarán solo si es local

    def mover(self, lista_obstaculos):
        # solo movemos con teclas el jugador local
        if not self.es_local or not self.controles:
            return
        #Inicializamos variables de movimiento
        teclas = pygame.key.get_pressed()
        dx, dy = 0, 0 #Dirección del movimiento direccion x, direccion y

        #Lista de controles
        if teclas[self.controles['arriba']]: dy = -self.velocidad
        if teclas[self.controles['abajo']]:  dy = self.velocidad
        if teclas[self.controles['izq']]:    dx = -self.velocidad
        if teclas[self.controles['der']]:    dx = self.velocidad

        # Movimiento en X con colisiones
        self.rect.x += dx
        if self.rect.left < 0 or self.rect.right > ANCHO or self.rect.collidelist(lista_obstaculos) != -1: # Colisión
            self.rect.x -= dx # Deshacer si choca

        # Movimiento en Y con colisiones
        self.rect.y += dy
        if self.rect.top < 0 or self.rect.bottom > ALTO or self.rect.collidelist(lista_obstaculos) != -1: # Colisión
            self.rect.y -= dy # Deshacer si choca

    # Método para actualizar posición cuando llega dato del Servidor
    def establecer_posicion(self, x, y):
        self.rect.x = x
        self.rect.y = y

    #Funcion para reiniciar la posicion del jugador
    def reiniciar_posicion(self):
        self.rect.topleft = (self.inicio_x, self.inicio_y)
    
    #Funcion para robar la bandera
    def robar(self, enemigo, bandera):
        # Lógica de intercepción de la bandera
        if self.rect.colliderect(enemigo.rect):
            if bandera.portador == enemigo:
                print(f"{self.NombreJugador} atrapó a {enemigo.NombreJugador}.")
                bandera.reiniciar()
                self.reiniciar_posicion() # El cazador vuelve a casa
                enemigo.reiniciar_posicion() # La victima vuelve a casa
                return True # Hubo robo
        return False # No hubo robo

    #Funcion para dibujar el jugador
    def dibujar(self, pantalla):
       # Color metálico oscuro para extremidades y detalles
        color_metal = (max(40, self.color[0]-60), max(40, self.color[1]-60), max(40, self.color[2]-60))
        # Color del visor brillante 
        if self.color != AMARILLO:
            color_visor = (100, 240, 255)
        else: #Si el jugador es amarillo cambia el color
            color_visor=(255, 50, 50) 
        # Definimos áreas relativas al tamaño del jugador (self.rect)
        cuerpo_ancho = self.rect.width - 4
        cuerpo_alto = self.rect.height - 10
        cuerpo_x = self.rect.centerx - cuerpo_ancho // 2
        cuerpo_y = self.rect.bottom - cuerpo_alto - 4
        # PIES
        pie_radio = 5
        pygame.draw.circle(pantalla, color_metal, (self.rect.left + 10, self.rect.bottom - 4), pie_radio)
        pygame.draw.circle(pantalla, color_metal, (self.rect.right - 10, self.rect.bottom - 4), pie_radio)
        # CUERPO PRINCIPAL
        cuerpo_rect = pygame.Rect(cuerpo_x, cuerpo_y, cuerpo_ancho, cuerpo_alto)
        pygame.draw.rect(pantalla, self.color, cuerpo_rect, border_radius=12)
        # Borde negro 
        pygame.draw.rect(pantalla, NEGRO, cuerpo_rect, 2, border_radius=12)
        # CABEZA y VISOR 
        # Un visor ancho y brillante en la parte superior del cuerpo
        visor_alto = 14
        visor_rect = pygame.Rect(cuerpo_rect.left + 4, cuerpo_rect.top + 6, cuerpo_rect.width - 8, visor_alto)
        pygame.draw.rect(pantalla, color_visor, visor_rect, border_radius=6)
         #Brillo del visor
        pygame.draw.line(pantalla, (255, 255, 255), (visor_rect.left + 4, visor_rect.top + 4), (visor_rect.right - 4, visor_rect.top + 4), 2)
        #ANTENAS
        # Dos pequeños círculos metálicos en la parte superior
        pygame.draw.circle(pantalla, color_metal, (cuerpo_rect.left + 8, cuerpo_rect.top + 2), 4)
        pygame.draw.circle(pantalla, color_metal, (cuerpo_rect.right - 8, cuerpo_rect.top + 2), 4)
        # Borde negro para las antenas
        pygame.draw.circle(pantalla, NEGRO, (cuerpo_rect.left + 8, cuerpo_rect.top + 2), 4, 1)
        pygame.draw.circle(pantalla, NEGRO, (cuerpo_rect.right - 8, cuerpo_rect.top + 2), 4, 1)