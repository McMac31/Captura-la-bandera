import pygame
from config import *

#Clase Bandera
class Bandera:
    def __init__(self):
        # Inicializamos la bandera
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.portador = None
        self.capturada = False

    #Funcion para que la bandera vuelva a la posicion inicial
    def reiniciar(self):
        self.portador = None
        self.rect.center = (ANCHO // 2, ALTO // 2)

    #Funcion para actualizar la posicion de la bandera
    def actualizar(self, jugador_rojo, jugador_azul):
        # Si nadie la tiene, comprobar si alguien la toca
        if self.portador is None:
            self.capturada = False
            if self.rect.colliderect(jugador_rojo.rect): #Si el jugador rojo la toca
                self.portador = jugador_rojo
                self.capturada = True
            elif self.rect.colliderect(jugador_azul.rect):#Si el jugador azul la toca
                self.portador = jugador_azul
                self.capturada = True
        
        # Si alguien la tiene, seguirlo
        else:
            self.rect.center = self.portador.rect.center

    #Funcion para dibujar la bandera
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, VERDE, self.rect) #La bandera es verde
        pygame.draw.rect(pantalla, NEGRO, self.rect, 2) #Borde de la bandera