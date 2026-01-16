import requests


class APIService:
    def __init__(self):
        # Base URL del servidor Spring Boot
        self.url_base = "http://35.171.209.196:8080/api"

    def registrar_jugador(self, nombre, email):
        try:
            r = requests.post(f"{self.url_base}/jugadores", json={"nombre": nombre, "email": email}, timeout=5)
            if r.status_code in (200, 201):
                # RETORNAR EL ID REAL QUE DA EL BACKEND
                return r.json().get("id") 
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con AWS: {e}")
            return None

    def get_ranking(self):
        try:
            #La URL del endpoint de ranking
            r = requests.get(f"{self.url_base}/jugadores/ranking", timeout=5)
            return r.json() if r.status_code == 200 else []
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con AWS: {e}")
            return []
        
    def get_partidas(self):
        try: #La URL del endpoint de partidas
            r = requests.get(f"{self.url_base}/partidas", timeout=5)
            return r.json() if r.status_code == 200 else []
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con AWS: {e}")
            return []

    def get_estadisticas_globales(self):
        try: #La URL del endpoint de estadísticas globales
            r = requests.get(f"{self.url_base}/estadisticas", timeout=5)
            return r.json() if r.status_code == 200 else {}
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con AWS: {e}")
            return {}

    def guardar_partida(self, datos_partida):
        try:
            # Bajamos el timeout para que el hilo no se quede colgado eternamente
            requests.post(f"{self.url_base}/partidas", json=datos_partida, timeout=2)
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con AWS: {e}")
    
    def get_jugadores(self):
        try: #La URL del endpoint de jugadores
            r = requests.get(f"{self.url_base}/jugadores", timeout=5)
            return r.json() if r.status_code == 200 else []
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con AWS: {e}")
            return []

    def get_historial_jugador(self, jugador_id):
        try: #La URL del endpoint de estadísticas de un jugador
            r = requests.get(f"{self.url_base}/jugadores/{jugador_id}/estadisticas", timeout=5)
            return r.json() if r.status_code == 200 else {}
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con AWS: {e}")
            return {}

    def eliminar_jugador(self, jugador_id):
        try: #La URL del endpoint para eliminar un jugador
            r = requests.delete(f"{self.url_base}/jugadores/{jugador_id}", timeout=5)
            return r.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con AWS: {e}")
            return False