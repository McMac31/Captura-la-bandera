import requests
from .odoo_servicio import OdooServicio
from .spring_boot_service import SpringBootServicio

class APIService:
    def __init__(self):
        # Inicializamos los servicios
        self.spring = SpringBootServicio()
        self.odoo = OdooServicio()
        # Base URL del servidor Spring Boot 
        self.url_base = self.spring.url_base

    def registrar_jugador(self, nombre, email):
        try:
            id_retorno = None
            # Buscamos si el correo ya existe para evitar duplicados y sumar puntos a la cuenta existente
            jugadores_existentes = self.get_jugadores()
            # Buscamos si el jugador tiene el mismo email 
            for j in jugadores_existentes:
                if j.get('email') == email:
                    # Si el correo coincide, guardamos el ID
                    id_retorno = j.get('id')
                    break 
            # Si no existe, lo creamos
            if id_retorno is None:
                r = requests.post(f"{self.url_base}/jugadores", json={"nombre": nombre, "email": email}, timeout=10)
                if r.status_code in (200, 201):
                    # Retorna el id de la BBDD
                    id_retorno = r.json().get("id")

            # SINCRONIZACIÓN CON ODOO 
            # Si tenemos un ID válido encontrado o creado, avisamos a Odoo
            if id_retorno:
                self.odoo.registrar_jugador(nombre, email,id_retorno)
                return id_retorno
            
            return None
        #Control de excepciones
        except requests.exceptions.RequestException as e:  #Control de excepciones
            print(f"Error de conexión con AWS: {e}")
            return None
        
    def iniciar_partida_odoo(self):
        #Funcion para poner el estado 'En Curso'
        return self.odoo.iniciar_partida()
    
    def finalizar_partida(self, datos_partida, odoo_id_partida):
        #Guarda en AWS y cierra la partida en Odoo 
        # Guardar en AWS (Ranking global)
        self.spring.guardar_partida(datos_partida)
        # Cerrar en Odoo (Historial y puntos)
        if odoo_id_partida:
            self.odoo.finalizar_partida(odoo_id_partida, datos_partida)

    def get_ranking(self):
        try:
            #La URL del endpoint de ranking
            r = requests.get(f"{self.url_base}/jugadores/ranking", timeout=5)
            return r.json() if r.status_code == 200 else []
        except requests.exceptions.RequestException as e: #Control de excepciones
            print(f"Error de conexión con AWS: {e}")
            return []
        
    def get_partidas(self):
        try: #La URL del endpoint de partidas
            r = requests.get(f"{self.url_base}/partidas", timeout=5)
            return r.json() if r.status_code == 200 else []
        except requests.exceptions.RequestException as e:  #Control de excepciones
            print(f"Error de conexión con AWS: {e}")
            return []

    def get_estadisticas_globales(self):
        try: #La URL del endpoint de estadísticas globales
            r = requests.get(f"{self.url_base}/estadisticas", timeout=5)
            return r.json() if r.status_code == 200 else {}
        except requests.exceptions.RequestException as e:  #Control de excepciones
            print(f"Error de conexión con AWS: {e}")
            return {}

    def guardar_partida(self, datos_partida):
        #Envío a AWS 
        try:
            # Bajamos el timeout para que el hilo no se quede colgado eternamente
            requests.post(f"{self.url_base}/partidas", json=datos_partida, timeout=2)
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con AWS: {e}")

        
        # Envío a Odoo 
        # Se hace fuera del try/except de AWS para que se intente enviar aunque AWS falle
        self.odoo.guardar_partida(datos_partida)
    
    def get_jugadores(self):
        try: #La URL del endpoint de jugadores
            r = requests.get(f"{self.url_base}/jugadores", timeout=5)
            return r.json() if r.status_code == 200 else []
        except requests.exceptions.RequestException as e:  #Control de excepciones
            print(f"Error de conexión con AWS: {e}")
            return []

    def get_historial_jugador(self, jugador_id):
        try: #La URL del endpoint de estadísticas de un jugador
            r = requests.get(f"{self.url_base}/jugadores/{jugador_id}/estadisticas", timeout=5)
            return r.json() if r.status_code == 200 else {}
        except requests.exceptions.RequestException as e:  #Control de excepciones
            print(f"Error de conexión con AWS: {e}")
            return {}

    def eliminar_jugador(self, jugador_id):
        try: #La URL del endpoint para eliminar un jugador
            r = requests.delete(f"{self.url_base}/jugadores/{jugador_id}", timeout=5)
            return r.status_code == 200
        except requests.exceptions.RequestException as e:  #Control de excepciones
            print(f"Error de conexión con AWS: {e}")
            return False