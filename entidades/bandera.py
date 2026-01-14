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

    def actualizar(self, lista_jugadores): #Recibe la lista de jugadores
        # Si nadie la tiene, comprobar si alguien la toca
        if self.portador is None:
            self.capturada = False
            for jugador in lista_jugadores:
                # Verificamos colisión con el rectángulo del jugador
                if self.rect.colliderect(jugador.rect):
                    self.portador = jugador
                    self.capturada = True
                    break # Solo un jugador puede cogerla a la vez
        
        # 2. Si alguien la tiene, la bandera sigue al jugador
        else:
            self.rect.center = self.portador.rect.center

    #Funcion para dibujar la bandera
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, VERDE, self.rect) #La bandera es verde
        pygame.draw.rect(pantalla, NEGRO, self.rect, 2) #Borde de la bandera