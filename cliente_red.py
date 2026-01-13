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
        self.buffer=""

    def conectar(self):
        #Intenta conectar al servidor y arranca el hilo de escucha.
        try:
            self.cliente.connect(DIRECCION_SERVIDOR)
            buffer_temp = ""
            while "\n" not in buffer_temp:
                datos_recibidos = self.cliente.recv(2048).decode("utf-8")
                if not datos_recibidos: raise Exception("Servidor cerró")
                buffer_temp += datos_recibidos
            
            msg_raw, resto = buffer_temp.split("\n", 1)
            self.buffer = resto # Guardamos lo que sobre para luego
            
            data = json.loads(msg_raw)
            
            if data["tipo"] == "BIENVENIDA":
                self.id = data["id"]
                self.conectado = True
                print(f"[RED] Conectado al servidor con ID: {self.id}")
                
                thread = threading.Thread(target=self.escuchar_servidor)
                thread.daemon = True 
                thread.start()
                return True
            #Control de excepciones
        except Exception as e:
            print(f"[RED] Error al conectar: {e}")
            return False
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
                # 1. Recibimos datos crudos
                datos_recibidos = self.cliente.recv(2048).decode("utf-8")
                if not datos_recibidos:
                    print("[RED] Servidor cerró conexión")
                    self.conectado = False
                    break
                
                # 2. Añadimos al buffer
                self.buffer += datos_recibidos
                
                # 3. Procesamos todos los mensajes completos que haya en el buffer
                while "\n" in self.buffer:
                    mensaje_completo, self.buffer = self.buffer.split("\n", 1)
                    if mensaje_completo.strip(): # Ignoramos líneas vacías
                        try:
                            data = json.loads(mensaje_completo)
                            self.cola_mensajes.append(data)
                        except json.JSONDecodeError:
                            print(f"[RED] Error JSON: {mensaje_completo}")

            except Exception as e:
                print(f"[RED] Desconectado: {e}")
                self.conectado = False
                break
            except socket.error as e: #Control error socket
                print(f"[RED] Error de socket: {e}")
                self.conectado = False
                break
            except json.JSONDecodeError as e: #Control error JSON
                print(f"[RED] Error decodificando JSON: {e}")
                break

    def enviar(self, data):
        # Envía un diccionario de datos al servidor.
        if self.conectado:
            try:
                mensaje = json.dumps(data) + "\n" # Convertir a JSON y añadir salto de línea
                self.cliente.send(mensaje.encode("utf-8")) # Convertir a JSON y enviar
            except socket.error as e: #Control error socket
                print(f"[RED] Error enviando: {e}")

    def obtener_mensajes(self):
        #Devuelve los mensajes pendientes y limpia la cola.
        mensajes = self.cola_mensajes[:]
        self.cola_mensajes = []
        return mensajes