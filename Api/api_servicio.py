import requests

class APIService:
    def __init__(self):
        # Base URL de tu servidor Spring Boot
        self.url_base = "http://35.171.209.196:8080/api"

    def registrar_jugador(self, nombre, email):
        try:
            r = requests.post(f"{self.url_base}/jugadores", json={"nombre": nombre, "email": email}, timeout=5)
            return r.status_code in (200, 201)
        except: return False

    def obtener_ranking(self):
        try:
            # Nota: La URL correcta según tu ApiPsql.py es /jugadores/ranking
            r = requests.get(f"{self.url_base}/jugadores/ranking", timeout=5)
            return r.json() if r.status_code == 200 else []
        except: return []

    def obtener_partidas(self):
        try:
            r = requests.get(f"{self.url_base}/partidas", timeout=5)
            return r.json() if r.status_code == 200 else []
        except: return []

    def obtener_estadisticas_globales(self):
        try:
            r = requests.get(f"{self.url_base}/estadisticas", timeout=5)
            return r.json() if r.status_code == 200 else {}
        except: return {}

    def guardar_partida(self, datos_partida):
        try:
            # Bajamos el timeout para que el hilo no se quede colgado eternamente
            requests.post(f"{self.url_base}/partidas", json=datos_partida, timeout=2)
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con AWS: {e}")