import threading
import requests

class OdooServicio:
    def __init__(self):
        self.url_base="http://mamtech.duckdns.org:8069/api/gamehub"
        
    def registrar_jugador(self,nombre,email): #Registro de jugador a Odoo
        def enviar(): #Enviar el jugador a Odoo
            try:
                requests.post(f"{self.url_base}/jugador", json={"nombre":nombre,"email":email}, timeout=5)
                print("[Odoo] Jugador Enviado")
            except Exception as e:
                print(f"[Odoo] Error enviando jugador {e}")

        # Lo hacemos en un hilo aparte para no frenar el juego si Odoo va lento
        threading.Thread(target=enviar, daemon=True).start()
    def guardar_partida(self,datos):
        #Enviamos la partida a Odoo
        def enviar():
            try:
                requests.post(f"{self.url_base}/partida",json=datos, timeout=5)
                print("[Odoo] Partida Enviada")
            except Exception as e:
                print(f"[Odoo] Error guardando partida: {e}")
            
        threading.Thread(target=enviar,daemon=True).start()