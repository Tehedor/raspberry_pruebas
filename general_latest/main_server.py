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

def sensor_task(task, sleeptime, stop_event):
    while not stop_event.is_set():
        task()
        time.sleep(sleeptime)

@app.route('/start', methods=['POST'])
def start_components():
    global components, threads, stop_event

    if threads:
        return jsonify({"status": "error", "message": "Components are already running"}), 400

    sleeptime = 0.05

    # Config components
    enable_street_light = True
    enable_toll = False
    enable_crane = False
    enable_weather_station = False
    enable_railroad_switch = False
    enable_radar = True

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

    return jsonify({"status": "success", "message": "Components started"}), 200

@app.route('/stop', methods=['POST'])
def stop_components():
    global components, threads, stop_event

    if not threads:
        return jsonify({"status": "error", "message": "Components are not running"}), 400

    stop_event.set()
    for thread in threads:
        thread.join()

    if components.get("street_light"):
        components["street_light"].destroy()
    if components.get("toll"):
        components["toll"].destroy()
    if components.get("crane"):
        components["crane"].destroy()
    if components.get("weather_station"):
        components["weather_station"].destroy()
    if components.get("radar"):
        components["radar"].destroy()
    if components.get("railroad_switch"):
        components["railroad_switch"].destroy()

    components = {}
    threads = []
    stop_event = threading.Event()

    return jsonify({"status": "success", "message": "Components stopped"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)