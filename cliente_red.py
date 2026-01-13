import socket
import threading
import json
from config import *

#Clase Cliente de Red
class ClienteRed:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Con AF_INET usamos IPv4, con SOCK_STREAM usamos TCP
        self.id = None # Mi ID asignado por el servidor
        self.cola_mensajes = [] # Buzón de mensajes recibidos
        self.conectado = False

    def conectar(self):
        #Intenta conectar al servidor y arranca el hilo de escucha.
        try:
            self.cliente.connect(DIRECCION_SERVIDOR) #Conectar al servidor
            # El primer mensaje es la BIENVENIDA con mi ID
            msg = self.cliente.recv(2048).decode("utf-8")
            data = json.loads(msg)
            
            if data["tipo"] == "BIENVENIDA":
                self.id = data["id"]
                self.conectado = True
                print(f"[RED] Conectado al servidor con ID: {self.id}")
                
                # Arrancamos el HILO DE ESCUCHA (daemon=True para que se cierre al salir)
                thread = threading.Thread(target=self.escuchar_servidor)
                thread.daemon = True 
                thread.start()
                return True
        except Exception as e:
            print(f"[RED] Error al conectar: {e}")
            return False
        except json.JSONDecodeError:
            print("[RED] Error decodificando mensaje de bienvenida")
            return False
        except ConnectionRefusedError:
            print("[RED] Conexión rechazada por el servidor")
            return False 
        except socket.error as e:
            print(f"[RED] Error de socket: {e}")
            return False
        except threading.ThreadError as e:
            print(f"[RED] Error al iniciar hilo de escucha: {e}")
            return False
        

    def escuchar_servidor(self):
        #Hilo que escucha mensajes del servidor.
        while self.conectado:
            try:
                mensaje = self.cliente.recv(2048).decode("utf-8") #Recibir mensaje
                if mensaje: 
                    try:
                        # Convertimos el texto JSON a diccionario
                        data = json.loads(mensaje)
                        self.cola_mensajes.append(data)
                    except json.JSONDecodeError:  #error JSON
                        print("[RED] Error decodificando mensaje JSON")
            except:
                print("[RED] Desconectado del servidor")
                self.conectado = False
                break

    def enviar(self, data):
        # Envía un diccionario de datos al servidor.
        if self.conectado:
            try:
                self.cliente.send(json.dumps(data).encode("utf-8")) # Convertir a JSON y enviar
            except socket.error as e: #Control error socket
                print(f"[RED] Error enviando: {e}")

    def obtener_mensajes(self):
        #Devuelve los mensajes pendientes y limpia la cola.
        mensajes = self.cola_mensajes[:]
        self.cola_mensajes = []
        return mensajes