import requests
class SpringBootServicio:
    def __init__(self):
        self.url_base = "http://35.171.209.196:8080/api"
    
    def registrar_jugador(self,nombre,email):
        try: #Control de excepciones
            registro= requests.post(f"{self.url_base}/jugadores",json={"nombre":nombre,"email":email}, timeout=5) #Enviamos los datos de registro
            if registro.status_code in (200,201): #En caso de exito
                return registro.json().get("id")
            return None
        except Exception as e: #En caso de error
            print(f"[BBDD]Error de conexion:{e}")
            return None
    
    def guardar_partida(self, datos):
        try: #Control de excepciones
            requests.post(f"{self.url_base}/partidas", json=datos, timeout=5) #Envio de datos
            print("[BBDD] Partida guardada.")
        except Exception as e:
            print(f"[BBDD] Error guardando: {e}")
        
    def get_all_jugadores(self):
        try:
            r = requests.get(f"{self.url_base}/jugadores", timeout=5)
            return r.json() if r.status_code == 200 else []
        except:
            return []
    