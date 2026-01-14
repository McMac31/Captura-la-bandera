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
        # SOLO nos movemos por teclado si somos el jugador local
        if not self.es_local or not self.controles:
            return
        #Inicializamos variables de movimiento
        teclas = pygame.key.get_pressed()
        dx, dy = 0, 0 #Dirección del movimiento

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
                print(f"¡Cazado! {self.color} atrapó a {enemigo.color}.")
                bandera.reiniciar()
                self.reiniciar_posicion()
                enemigo.reiniciar_posicion()

    #Funcion para dibujar el jugador
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        pygame.draw.rect(pantalla, NEGRO, self.rect, 2)