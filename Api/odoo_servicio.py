import threading
import requests

class OdooServicio:
    def __init__(self):
        self.url_base="http://mamtech.duckdns.org:8069/api/gamehub"
        
    def registrar_jugador(self, nombre, email, game_id):
        #Registra al jugador enviando también el ID de AWS (game_id)
        def enviar():
            try:
                requests.post(f"{self.url_base}/jugador", json={"nombre": nombre, "email": email, "game_id": game_id}, timeout=5)
                print(f"[Odoo] Jugador {nombre} sincronizado (GameID: {game_id}).")
            except Exception as e:
                print(f"[Odoo] Error al registrar jugador: {e}")
        
        threading.Thread(target=enviar, daemon=True).start()

    def iniciar_partida(self):
        #Avisa a Odoo que la partida EMPIEZA.
        #Retorna el ID de la partida creada en Odoo (ej: 45) o None si falla.
        try:
            print("[Odoo] Solicitando iniciar partida...")
            r = requests.post(f"{self.url_base}/partida/iniciar", json={}, timeout=2)
            
            if r.status_code == 200:
                id_partida = r.json().get('id')
                print(f"[Odoo] ✅ Partida iniciada. ID Odoo: {id_partida}")
                return id_partida
            else:
                print(f"[Odoo] ❌ Error al iniciar: {r.text}")
                return None
        except Exception as e:
            print(f"[Odoo] Error de conexión al iniciar: {e}")
            return None

    def finalizar_partida(self, odoo_id, datos):
        #Avisa a Odoo que la partida TERMINÓ.
        #Envia puntuaciones y cierra la sesión.
       
        def enviar():
            try:
                # Añadimos el ID que nos dio Odoo al principio
                datos['odoo_partida_id'] = odoo_id
                print(f"[Odoo] Enviando datos finales para partida {odoo_id}...")
                
                r = requests.post(f"{self.url_base}/partida/finalizar", json=datos, timeout=5)
                
                if r.status_code == 200:
                    print("[Odoo] ✅ Partida cerrada y puntos guardados.")
                else:
                    print(f"[Odoo] ❌ Error al cerrar: {r.text}")
            except Exception as e:
                print(f"[Odoo] Error al finalizar: {e}")
        
        # Lo hacemos en un hilo aparte para no frenar el servidor
        threading.Thread(target=enviar, daemon=True).start()