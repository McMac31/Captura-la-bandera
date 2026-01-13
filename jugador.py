import pygame
from config import *

#Clase Jugador
class Jugador:
    def __init__(self, x, y, color, controles):
        # Inicializamos atributos del jugador
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.controles = controles
        self.velocidad = 6
        self.puntos = 0 #Punrtuacion del jugador
        # Guardamos posición inicial
        self.inicio_x = x
        self.inicio_y = y

    # Función para mover al jugador
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

    # Función para reiniciar la posición del jugador
    def reiniciar_posicion(self):
        self.rect.topleft = (self.inicio_x, self.inicio_y)
    
    #Función para intentar robar la bandera al enemigo
    def intentar_robar(self, enemigo, bandera):
        # Lógica de intercepción de la bandera
        if self.rect.colliderect(enemigo.rect):
            if bandera.portador == enemigo:
                print(f"¡Cazado! {self.color} atrapó a {enemigo.color}.")
                bandera.reiniciar()
                self.reiniciar_posicion()
                enemigo.reiniciar_posicion()

    # Función para dibujar al jugador
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        pygame.draw.rect(pantalla, NEGRO, self.rect, 2)