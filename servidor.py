import socket
import threading
import json
import time
from config import *

#Clase Servidor de Red
class Servidor:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Con AF_INET usamos IPv4, con SOCK_STREAM usamos TCP
        self.server.bind(DIRECCION_SERVIDOR) #Enlazamos el socket a la direccion y puerto
        self.server.listen() #Ponemos el servidor en modo escucha
        
        print(f"[ARRANCANDO] Servidor escuchando en {SERVIDOR_IP}:{PUERTO}")

        self.clientes = [] # Lista de sockets conectados
        self.direcciones = {} # Mapa de direcciones {socket: direccion}
        self.jugadores_info = {} # Datos del juego {id_jugador: {x, y, color...}}
        
        # ID para asignar a los jugadores según van llegando (1, 2, 3, 4)
        self.id_actual = 1 
    
    #Funcion para manejar a un cliente
    def manejar_cliente(self, conexion, direccion, id_jugador):
        #Hilo individual para gestionar a UN cliente.
        print(f"[NUEVA CONEXIÓN] {direccion} conectado. Asignado ID: {id_jugador}")
        conectado= True
        try:
            while conectado:
                # Esperar mensaje del cliente
                msg = conexion.recv(2048).decode("utf-8")
                if not msg:
                    break
                # Procesar JSON
                data = json.loads(msg)
                
                # Protocolo simple: Si recibo datos, los actualizo en mi "base de datos"
                if "posicion" in data:
                    self.jugadores_info[id_jugador] = data["posicion"]
                    
                    # REENVIAR (Broadcast) a todos los demas
                    self.broadcast_estado(id_jugador, data)

        except Exception as e: #Control de errores
            print(f"[ERROR] Con el cliente {id_jugador}: {e}")
        except json.JSONDecodeError:
            print(f"[ERROR] JSON inválido recibido del cliente {id_jugador}.")
        except ConnectionResetError:
            print(f"[DESCONECTADO] Cliente {id_jugador} se desconectó abruptamente.")
        
        finally:
            # Desconexión limpia
            print(f"[DESCONECTADO] Cliente {id_jugador} se fue.")
            self.clientes.remove(conexion)
            del self.jugadores_info[id_jugador]
            conexion.close()

    def broadcast_estado(self, id_origen, data):
        #Envía información a todos los clientes
        mensaje_json = json.dumps(data) # Convertir a JSON
        
        for cliente in self.clientes:
            try:
                cliente.sendall(mensaje_json.encode("utf-8"))
            except:
                self.clientes.remove(cliente)

    def iniciar(self):
        #Bucle principal que acepta conexiones
        print("[ESPERANDO CONEXIONES]...")
        while True:
            if len(self.clientes) < 4: # Limite de 4 jugadores
                conexion, direccion = self.server.accept()
                self.clientes.append(conexion)
                
                # Enviar mensaje de BIENVENIDA con su ID
                paquete_bienvenida = {"tipo": "BIENVENIDA", "id": self.id_actual}
                conexion.send(json.dumps(paquete_bienvenida).encode("utf-8"))
                
                # Arrancar un HILO (THREAD) para este cliente
                thread = threading.Thread(target=self.manejar_cliente, args=(conexion, direccion, self.id_actual))
                thread.start()
                
                self.id_actual += 1
                print(f"[CLIENTES ACTIVOS] {threading.active_count() - 1}")
            else:
                pass

if __name__ == "__main__":
    s = Servidor()
    s.iniciar()