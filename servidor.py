import socket
import threading
import json
import time
import requests
from config import *

#Clase Servidor de Red
class Servidor:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Con AF_INET usamos IPv4, con SOCK_STREAM usamos TCP
        self.server.bind(DIRECCION_SERVIDOR) #Enlazamos el socket a la direccion y puerto
        self.server.listen() #Ponemos el servidor en modo escucha
        
        print(f"[ARRANCANDO] Servidor escuchando en {SERVIDOR_IP}:{PUERTO}") #Validamos que el servidor esta corriendo

        self.clientes = [] # Lista de sockets conectados
        self.direcciones = {} # Mapa de direcciones {socket: direccion}
        self.jugadores_info = {} # Datos del juego {id_jugador: {x, y, color...}}
        
        # Maximo 4 jugadores (IDs del 1 al 4)
        self.ids_disponibles = [1, 2, 3, 4] 
        
        # Control de la Bandera
        self.dueno_bandera = None # ID del jugador que tiene la bandera actualmente

        # Generamos el mapa una sola vez para enviarlo a todos
        self.mapa_obstaculos = [(m.x, m.y, m.w, m.h) for m in OBSTACULOS]

        self.tiempo_inicio_sesion = None
        self.historial_puntos = {} # Guardará {id_jugador: puntos}
        self.ids_jugadores_sesion = set() # Todos los que pasaron por la partida
    
    #Funcion para manejar a un cliente
    def manejar_cliente(self, conexion, direccion, id_jugador):
        print(f"[CONEXIÓN] {direccion} ID: {id_jugador}")
        # Iniciamos contador de tiempo y puntos apenas entra el primer jugador
        if not self.clientes:
            self.tiempo_inicio_sesion = time.time()
            self.historial_puntos = {}
            self.ids_jugadores_sesion = set()
        
        self.ids_jugadores_sesion.add(id_jugador)
        buffer = "" 
        try: #Control de excepciones
            while True:
                datos_recibidos = conexion.recv(2048).decode("utf-8") #Recibimos datos del cliente
                if not datos_recibidos: break
                buffer += datos_recibidos
                # Procesamos mensajes completos separados por \n
                while "\n" in buffer:
                    mensaje, buffer = buffer.split("\n", 1) 
                    if not mensaje.strip(): continue
                    
                    try:
                        data = json.loads(mensaje) #Decodificamos el JSON recibido
                        
                        # Si es un evento especial
                        if "evento" in data:
                            # Si alguien pide la bandera
                            if data["evento"] == "PETICION":
                                # Solo se la damos si NADIE la tiene
                                if self.dueno_bandera is None:
                                    self.dueno_bandera = id_jugador
                                    
                                    # controlamos quien tiene la bandera
                                    msg_oficial = {"evento": "COGER", "id": id_jugador}
                                    self.broadcast_estado(id_jugador, msg_oficial)
                            
                            # Si hay un reset
                            elif data["evento"] == "RESET":
                                self.dueno_bandera = None
                                self.broadcast_estado(id_jugador, data)

                        # Si es movimiento normal, retransmitimos
                        elif "posicion" in data:
                            self.jugadores_info[id_jugador] = data["posicion"]
                            self.broadcast_estado(id_jugador, data)
                            
                    except json.JSONDecodeError:
                        print(f"[ERROR JSON] Cliente {id_jugador}: {mensaje}")
        #Control de excepciones
        except Exception as e:
            print(f"[ERROR] Cliente {id_jugador}: {e}")
        except socket.error as e:
            print(f"[ERROR DE SOCKET] Cliente {id_jugador}: {e}")
        except json.JSONDecodeError as e:    
            print(f"[ERROR JSON] Cliente {id_jugador}: {e}")
        # Cerramos la conexion del cliente
        finally:
            print(f"[SALIDA] Cliente {id_jugador} desconectado")
            if conexion in self.clientes:
                self.clientes.remove(conexion)
            
            # Si ya no queda nadie, enviamos a AWS
            if not self.clientes and self.tiempo_inicio_sesion:
                self.finalizar_partida_aws()
            if conexion in self.clientes:
                self.clientes.remove(conexion)
            if id_jugador in self.jugadores_info:
                del self.jugadores_info[id_jugador]
            
            # Recuperamos la ID para que otro la pueda usar
            if id_jugador not in self.ids_disponibles:
                self.ids_disponibles.append(id_jugador)
                self.ids_disponibles.sort() # Ordenamos para que siempre se asigne la mas baja
            
            # Avisamos a todos de que este jugador se fue (para borrar su muñeco)
            self.broadcast_estado(id_jugador, {"evento": "SALIDA", "id": id_jugador})

            # Si se va el que tiene la bandera, la liberamos Y AVISAMOS
            if self.dueno_bandera == id_jugador:
                self.dueno_bandera = None
                self.broadcast_estado(id_jugador, {"evento": "RESET"})

            conexion.close()

    def broadcast_estado(self, id_origen, data):
        mensaje = json.dumps(data) + "\n"
        
        for cliente in self.clientes:
            try:
                cliente.sendall(mensaje.encode("utf-8"))
            except:
                pass # Si falla, se encargará el hilo de ese cliente de borrarlo

    def iniciar(self):
        print("[ESPERANDO JUGADORES]...")
        while True:
            # Aceptamos conexion
            conexion, direccion = self.server.accept()
            
            # Solo dejamos entrar si hay IDs disponibles 
            if len(self.ids_disponibles) > 0:
                # Asignamos la ID más baja disponible
                id_asignada = self.ids_disponibles.pop(0)
                self.clientes.append(conexion)
                
                # Mensaje de bienvenida CON EL MAPA
                bienvenida = json.dumps({
                    "tipo": "BIENVENIDA",
                    "id": id_asignada,
                    "mapa": self.mapa_obstaculos
                }) + "\n"
                conexion.send(bienvenida.encode("utf-8")) 
                
                # Sincronizamos al nuevo jugador si alguien ya tiene la bandera
                if self.dueno_bandera is not None:
                     msg_estado = {"evento": "COGER", "id": self.dueno_bandera}
                     conexion.send((json.dumps(msg_estado) + "\n").encode("utf-8"))

                thread = threading.Thread(target=self.manejar_cliente, args=(conexion, direccion, id_asignada)) #Hilo para manejar al cliente
                thread.start() #Iniciamos el hilo
            else:
                print(f"Rechazada conexión de {direccion}: Sala llena")
                conexion.close()
    
    def finalizar_partida_aws(self):
        duracion = int(time.time() - self.tiempo_inicio_sesion)
        # Preparamos las listas basadas en lo que recolectamos
        ids = list(self.ids_jugadores_sesion)
        # Obtenemos los puntos de cada uno (si no enviaron nada, ponemos 0)
        puntajes = [self.historial_puntos.get(pid, 0) for pid in ids]
        
        # Buscamos quién tuvo más puntos para el campo "id" (ganador)
        id_ganador = ids[0] if ids else 0
        if puntajes:
            max_puntaje = max(puntajes)
            indice_ganador = puntajes.index(max_puntaje)
            id_ganador = ids[indice_ganador]

        datos_finales = {
            "duracion": duracion,
            "id": id_ganador,
            "jugadorIds": ids,
            "puntajes": puntajes
        }

        print(f"[AWS] Sala vacía. Enviando partida final de {duracion}s...")
        try:
            # URL de Spring Boot
            requests.post("http://35.171.209.196:8080/api/partidas", json=datos_finales, timeout=5)
            print("[AWS] Partida guardada con éxito.")
        except Exception as e:
            print(f"[AWS] Error al guardar: {e}")
        
        # Reset para la próxima partida
        self.tiempo_inicio_sesion = None
        def envio_seguro(): # Envío en hilo aparte
            try:
                print("[AWS] Guardando historial final...")
                # Esta llamada puede tardar segundos si la red va lenta
                requests.post("http://35.171.209.196:8080/api/partidas", json=datos_finales, timeout=10)
                print("[AWS] Éxito: Partida guardada.")
            except Exception as e:
                print(f"[AWS] Error: No se pudo guardar la sesión: {e}")
        # Lanzamos la tarea en un hilo aparte para que el servidor siga libre
        # Esto facilita que si alguien intenta entrar justo ahora, el servidor responda al instante
        hilo_aws = threading.Thread(target=envio_seguro, daemon=True) # Daemon para que no bloquee la salida
        hilo_aws.start() #Iniciamos el hilo

if __name__ == "__main__":
    s = Servidor()
    s.iniciar()