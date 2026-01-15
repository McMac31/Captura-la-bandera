import threading
from flask import Flask, jsonify, render_template
import os
from API.api_servicio import APIService

class ServerFlask(threading.Thread):
    def __init__(self, juego_instancia):
        # Inicializamos el hilo
        super().__init__() # Llamada al constructor padre
        # Guardamos la referencia al juego para acceder a sus datos (id, jugadores, bandera)
        self.juego = juego_instancia
        self.daemon = True # El hilo muere automáticamente cuando se cierra el juego

    def run(self):
        # Esta función se ejecuta al hacer .start() desde el juego
        base_dir = os.path.dirname(__file__)
        template_dir = os.path.abspath(os.path.join(base_dir, 'templates'))
        # --- NUEVO: Definimos la carpeta de archivos estaticos (CSS) ---
        static_dir = os.path.abspath(os.path.join(base_dir, 'static'))
        
        # Iniciamos Flask con las carpetas configuradas
        app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

        # Ruta Principal Muestra la página web
        @app.route('/')
        def inicio():
            # Pasamos el objeto juego a la plantilla
            api=APIService()
            ranking=api.obtener_ranking()
            return render_template('index.html', juego=self.juego, ranking=ranking)

        # Ruta API: Devuelve el estado del juego en JSON 
        @app.route('/api/estado')
        def get_estado():
            datos_jugadores = []
            # Hacemos una copia de los jugadores para evitar problemas de concurrencia
            copia_jugadores = list(self.juego.jugadores.values())
            
            for j in copia_jugadores:
                datos_jugadores.append({
                    "id": j.id,
                    "nombre": j.NombreJugador,
                    "puntos": j.puntos,
                    "posicion": {"x": j.rect.x, "y": j.rect.y},
                    "es_local": j.es_local
                })
            
            # Estado de la bandera
            info_bandera = {
                "capturada": self.juego.bandera.capturada,
                "portador_id": self.juego.bandera.portador.id if self.juego.bandera.portador else None,
                "posicion": {"x": self.juego.bandera.rect.x, "y": self.juego.bandera.rect.y}
            }

            return jsonify({
                "mi_id_local": self.juego.mi_id,
                "total_jugadores": len(datos_jugadores),
                "jugadores": datos_jugadores,
                "bandera": info_bandera
            })

        @app.route('/ranking')
        def ver_ranking():
            api = APIService()
            datos_ranking = api.obtener_ranking()
            # Usamos el template ranking.html que ya tienes creado
            return render_template('ranking.html', ranking=datos_ranking)

        @app.route('/partidas')
        def ver_partidas():
            api = APIService()
            lista_partidas = api.obtener_partidas()
            # Aquí podrías crear un template partidas.html
            return jsonify(lista_partidas) 

        @app.route('/estadisticas')
        def ver_stats():
            api = APIService()
            stats = api.obtener_estadisticas_globales()
            return jsonify(stats)

        # Configuración del puerto dinámico basado en ID
        puerto = 5000 + self.juego.mi_id
        print(f" Servidor iniciado en http://localhost:{puerto}")
        
        # Ejecutamos Flask
        app.run(host='0.0.0.0', port=puerto, debug=True, use_reloader=False)