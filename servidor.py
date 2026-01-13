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
        print(f"[CONEXIÓN] {direccion} ID: {id_jugador}")
        buffer = ""
        try:
            while True:
                datos_recibidos = conexion.recv(2048).decode("utf-8")
                if not datos_recibidos: break
                buffer += datos_recibidos
                # Procesamos mensajes completos separados por \n
                while "\n" in buffer:
                    mensaje, buffer = buffer.split("\n", 1)
                    if not mensaje.strip(): continue
                    
                    try:
                        data = json.loads(mensaje)
                        
                        if "posicion" in data:
                            self.jugadores_info[id_jugador] = data["posicion"]
                            self.broadcast_estado(id_jugador, data)
                            
                    except json.JSONDecodeError:
                        print(f"[ERROR JSON] Cliente {id_jugador}: {mensaje}")

        except Exception as e:
            print(f"[ERROR] Cliente {id_jugador}: {e}")
        except socket.error as e:
            print(f"[ERROR DE SOCKET] Cliente {id_jugador}: {e}")
        except json.JSONDecodeError as e:    
            print(f"[ERROR JSON] Cliente {id_jugador}: {e}")
        
        finally:
            print(f"[SALIDA] Cliente {id_jugador} desconectado")
            if conexion in self.clientes:
                self.clientes.remove(conexion)
            if id_jugador in self.jugadores_info:
                del self.jugadores_info[id_jugador]
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
            if len(self.clientes) < 4:
                conexion, direccion = self.server.accept()
                self.clientes.append(conexion)
                
                # ENVIAMOS BIENVENIDA CON \n
                bienvenida = json.dumps({"tipo": "BIENVENIDA", "id": self.id_actual}) + "\n"
                conexion.send(bienvenida.encode("utf-8"))
                thread = threading.Thread(target=self.manejar_cliente, args=(conexion, direccion, self.id_actual))
                thread.start()
                
                self.id_actual += 1
            else:
                pass

if __name__ == "__main__":
    s = Servidor()
    s.iniciar()