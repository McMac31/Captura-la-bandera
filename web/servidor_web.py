import threading
from flask import Flask, app, jsonify, render_template, redirect, url_for
import os
from API.api_servicio import APIService

class ServerFlask(threading.Thread):
    def __init__(self, servidor_servidor):
        # Inicializamos el hilo
        super().__init__() # Llamada al constructor padre
        # Guardamos la referencia al servidor para acceder a sus datos
        self.servidor = servidor_servidor
        self.daemon = True # El hilo muere automáticamente cuando se cierra el servidor

    def run(self):
        # Esta función se ejecuta al hacer .start() desde el servidor
        base_dir = os.path.dirname(__file__)
        template_dir = os.path.abspath(os.path.join(base_dir, 'templates'))
        # Definimos la carpeta de archivos estaticos (CSS, JS, imágenes)
        static_dir = os.path.abspath(os.path.join(base_dir, 'static'))
        
        # Iniciamos Flask con las carpetas configuradas
        app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

        # Ruta Principal Muestra la página web
        @app.route('/')
        def inicio():
            return render_template('index.html', servidor=self.servidor)

        # Ruta API: Devuelve el estado del servidor en JSON 
        @app.route('/api/estado')
        def get_estado():
            datos_jugadores = []
            for id_j, info in self.servidor.jugadores_info.items():
                datos_jugadores.append({
                    "id": id_j,
                    "nombre": info.get('nombre', f"Jugador {id_j}"),
                    "puntos": self.servidor.historial_puntos.get(id_j, 0),
                    "posicion": info.get('posicion', {"x": 0, "y": 0})
                })
            pos_bandera = {"x": 400, "y": 300} # Por defecto centro
            if self.servidor.dueno_bandera:
                # Si hay portador, la bandera está donde esté el jugador
                info_p = self.servidor.jugadores_info.get(self.servidor.dueno_bandera)
                if info_p and "posicion" in info_p:
                    pos_bandera = info_p["posicion"]

            info_bandera = {
                "capturada": self.servidor.dueno_bandera is not None,
                "portador_id": self.servidor.dueno_bandera,
                "posicion": pos_bandera
            }

            return jsonify({
                "total_jugadores": len(datos_jugadores),
                "jugadores": datos_jugadores,
                "bandera": info_bandera
            })

        @app.route('/ranking')
        def ver_ranking():
            api = APIService()
            datos_ranking = api.get_ranking()
            # Usamos el template ranking.html 
            return render_template('ranking.html', ranking=datos_ranking)

        @app.route('/partidas')
        def ver_partidas():
            api = APIService()
            lista_partidas = api.get_partidas() # Obtenemos las partidas (tienen IDs)
            lista_jugadores = api.get_jugadores() # Obtenemos todos los jugadores (tienen Nombres e IDs)
            
            # Creamos un diccionario para buscar rápido: {id: nombre}
            nombres_map = {j['id']: j['nombre'] for j in lista_jugadores}
            # Reemplazando los IDs por nombres
            for p in lista_partidas:
                # Creamos una nueva lista con los nombres correspondientes a cada ID
                ids = p.get('jugadorIds', [])
                p['nombres_jugadores'] = [nombres_map.get(jid, f"ID {jid}") for jid in ids]
            
            # Pasamos la lista procesada al template
            return render_template('partidas.html', partidas=lista_partidas)

        @app.route('/estadisticas')
        def ver_stats():
            api = APIService()
            datos_stats = api.get_estadisticas_globales()
            # Usamos el template estadisticas.html
            return render_template('estadisticas.html', stats=datos_stats)

        @app.route('/eliminar/<int:id_jugador>')
        def borrar_jugador(id_jugador):
            api = APIService()
            if api.eliminar_jugador(id_jugador): #
                return redirect(url_for('ver_ranking'))
            return f"Error al eliminar al jugador {id_jugador}", 500

        # El servidor central siempre corre en el puerto 5000
        print(f" Servidor iniciado en http://localhost:5000")
        
        # Ejecutamos Flask
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)