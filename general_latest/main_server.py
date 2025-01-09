import time
import threading
from flask import Flask, jsonify
from dotenv import load_dotenv

from server.server_iot import IoTServer
from components.streetlight import StreetLight
from components.toll.toll import Toll
from components.crane import Crane
from components.weatherStation import WeatherStation
from components.railroadSwitch import RailroadSwitch
from components.radar import Radar

# Inicialización de Flask y carga de variables de entorno
app = Flask(__name__)
load_dotenv()

# Variables globales para gestionar los componentes, hilos y estado
components = {}
threads = []
stop_event = threading.Event()
state = "stopped"

# Tiempo entre iteraciones de las tareas
SLEEPTIME = 0.05

# Configuración de habilitación de componentes
ENABLE_STREET_LIGHT = True
ENABLE_TOLL = False
ENABLE_CRANE = False
ENABLE_WEATHER_STATION = False
ENABLE_RAILROAD_SWITCH = False
ENABLE_RADAR = True


def configure_components():
    """
    Configura los componentes IoT según los valores de habilitación.
    """
    return {
        "street_light": StreetLight(pir_led_pin=22, pir_sensor_pin=18, photo_led_pin=27, threshold=128) if ENABLE_STREET_LIGHT else None,
        "toll": Toll(toll_pin=23) if ENABLE_TOLL else None,
        "crane": Crane(pin_ultrasound_trig=16, pin_ultrasound_echo=26) if ENABLE_CRANE else None,
        "weather_station": WeatherStation(pin_weatherSensor=17, sleeptime=SLEEPTIME) if ENABLE_WEATHER_STATION else None,
        "railroad_switch": RailroadSwitch(pin_switch=20, pin_servo=21) if ENABLE_RAILROAD_SWITCH else None,
        "radar": Radar(pin_button=19) if ENABLE_RADAR else None,
    }


def sensor_task(task, sleeptime, stop_event):
    """
    Ejecuta una tarea en un bucle hasta que se active el evento de detención.
    """
    while not stop_event.is_set():
        task()
        time.sleep(sleeptime)


@app.route('/start', methods=['POST'])
def start_components():
    """
    Endpoint para iniciar los componentes IoT.
    """
    global components, threads, stop_event, state

    if threads:
        return jsonify({"status": "error", "message": "Components are already running"}), 400

    print("Starting components...")

    components = configure_components()

    # Crear y lanzar hilos para cada tarea habilitada
    stop_event.clear()
    tasks = []

    if components["street_light"]:
        tasks.append(components["street_light"].control_lights_server)
    if components["toll"]:
        tasks.append(components["toll"].read_card_server)
    if components["crane"]:
        tasks.append(components["crane"].detect_distance_server)
    if components["weather_station"]:
        tasks.append(components["weather_station"].detect_temperature_server)
    if components["radar"]:
        tasks.append(components["radar"].control_button_server)
    if components["railroad_switch"]:
        tasks.append(components["railroad_switch"].control_switch_server)

    threads = [
        threading.Thread(target=sensor_task, args=(task, SLEEPTIME, stop_event))
        for task in tasks
    ]

    for thread in threads:
        thread.start()

    state = "running"
    print("Components started.")
    return jsonify({"status": "success", "message": "Components started"}), 200


@app.route('/stop', methods=['POST'])
def stop_components():
    """
    Endpoint para detener los componentes IoT.
    """
    global components, threads, stop_event, state

    if not threads:
        return jsonify({"status": "error", "message": "Components are not running"}), 400

    print("Stopping components...")
    stop_event.set()

    # Esperar a que los hilos terminen
    for thread in threads:
        thread.join()

    # Destruir los componentes
    for component in components.values():
        if component:
            component.destroy()

    components.clear()
    threads.clear()
    state = "stopped"
    print("Components stopped.")
    return jsonify({"status": "success", "message": "Components stopped"}), 200


@app.route('/status', methods=['GET'])
def get_status():
    """
    Endpoint para obtener el estado de los componentes.
    """
    global state
    return jsonify({"status": "success", "state": state}), 200


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
