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

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file

# Global variables to manage the components and threads
components = {}
threads = []
stop_event = threading.Event()

state = "stop"

def sensor_task(task, sleeptime, stop_event):
    while not stop_event.is_set():
        task()
        time.sleep(sleeptime)

sleeptime = 0.05
    # Config components
enable_street_light = True
enable_toll = False
enable_crane = False
enable_weather_station = False
enable_railroad_switch = False
enable_radar = True
    
@app.route('/start', methods=['POST'])
def start_components():
    global components, threads, stop_event, state

    if threads:
        return jsonify({"status": "error", "message": "Components are already running"}), 400

    street_light = StreetLight(pir_led_pin=22, pir_sensor_pin=18, photo_led_pin=27, threshold=128) if enable_street_light else None
    toll = Toll(toll_pin=23) if enable_toll else None
    crane = Crane(pin_ultrasound_trig=16, pin_ultrasound_echo=26) if enable_crane else None
    railroad_switch = RailroadSwitch(pin_switch=20, pin_servo=21) if enable_railroad_switch else None
    radar = Radar(pin_button=19) if enable_radar else None
    weather_station = WeatherStation(pin_weatherSensor=17, sleeptime=sleeptime) if enable_weather_station else None

    server = IoTServer(
        street_light=street_light,
        toll=toll,
        crane=crane,
        weather_station=weather_station,
        railroad_switch=railroad_switch,
        radar=radar,
    )

    components = {
        "street_light": street_light,
        "toll": toll,
        "crane": crane,
        "weather_station": weather_station,
        "railroad_switch": railroad_switch,
        "radar": radar,
        "server": server
    }

    tasks = [server.run]
    if enable_street_light:
        tasks.append(street_light.control_lights_server)
    if enable_toll:
        tasks.append(toll.read_card_server)
    if enable_crane:
        tasks.append(crane.detect_distance_server)
    if enable_weather_station:
        tasks.append(weather_station.detect_temperature_server)
    if enable_radar:
        tasks.append(radar.control_button_server)
    if enable_railroad_switch:
        tasks.append(railroad_switch.control_switch_server)

    stop_event = threading.Event()
    threads = []
    for task in tasks:
        thread = threading.Thread(target=sensor_task, args=(task, sleeptime, stop_event))
        thread.start()
        threads.append(thread)

    state = "start"

    return jsonify({"status": "success", "message": "Components started"}), 200

@app.route('/stop', methods=['POST'])
def stop_components():
    global components, threads, stop_event, state

    if not threads:
        return jsonify({"status": "error", "message": "Components are not running"}), 400

    print("Stopping components...")

    # Señalar a los hilos que deben detenerse
    stop_event.set()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        print(f"Joining thread {thread.name}...")
        thread.join()
        print(f"Thread {thread.name} has stopped.")

    # Destruir los objetos de los componentes
    if components.get("street_light"):
        print("Destroying street_light...")
        try:
            components["street_light"].destroy()
        except Exception as e:
            print(f"Error destroying street_light: {e}")
    if components.get("toll"):
        print("Destroying toll...")
        try:
            components["toll"].destroy()
        except Exception as e:
            print(f"Error destroying toll: {e}")
    if components.get("crane"):
        print("Destroying crane...")
        try:
            components["crane"].destroy()
        except Exception as e:
            print(f"Error destroying crane: {e}")
    if components.get("weather_station"):
        print("Destroying weather_station...")
        try:
            components["weather_station"].destroy()
        except Exception as e:
            print(f"Error destroying weather_station: {e}")
    if components.get("radar"):
        print("Destroying radar...")
        try:
            components["radar"].destroy()
        except Exception as e:
            print(f"Error destroying radar: {e}")
    if components.get("railroad_switch"):
        print("Destroying railroad_switch...")
        try:
            components["railroad_switch"].destroy()
        except Exception as e:
            print(f"Error destroying railroad_switch: {e}")

    # Limpiar las variables globales
    components = {}
    threads = []
    stop_event = threading.Event()
    state = "stop"

    print("Components stopped.")
    return jsonify({"status": "success", "message": "Components stopped"}), 200

@app.route('/status', methods=['GET'])
def get_status():
    global state

    status = {"state": state}
    return jsonify(status), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)