import requests

class APIService:
    def __init__(self):
        self.url_base = "http://35.171.209.196:8080/api"

    def registrar_jugador(self, nombre, email):
        #Lógica de postJugador.py integrada
        try:
            r = requests.post(f"{self.url_base}/jugadores", json={"nombre": nombre, "email": email}, timeout=5)
            return r.status_code in (200, 201)
        except: return False

    def obtener_ranking(self):
        #Lógica de getRanking.py integrada
        try:
            r = requests.get(f"{self.url_base}/ranking", timeout=5)
            return r.json() if r.status_code == 200 else []
        except: return []

    def guardar_partida(self, datos_partida):
        #Lógica de postPartida.py integrada
        try:
            requests.post(f"{self.url_base}/partidas", json=datos_partida, timeout=5)
        except: pass












