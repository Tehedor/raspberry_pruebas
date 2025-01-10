from flask import Flask, request, jsonify
from dotenv import load_dotenv
import time
import threading

from components.streetlight import StreetLight
from components.toll.toll import Toll
from components.crane import Crane
from components.weatherStation import WeatherStation
from components.railroadSwitch import RailroadSwitch
from components.radar import Radar


app = Flask(__name__)
load_dotenv()

# Global state of components
mode = "stopped"
stop_event = threading.Event()
components = {}
threads = []


# Tiempo entre iteraciones de las tareas
SLEEPTIME = 0.05

# Configuración de habilitación de componentes
IOT_INIT = {
    "ENABLE_STREET_LIGHT": True,
    "ENABLE_TOLL": False,
    "ENABLE_CRANE": False,
    "ENABLE_WEATHER_STATION": False,
    "ENABLE_RAILROAD_SWITCH": False,
    "ENABLE_RADAR": True
}

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
# IOT configuration
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
def sensor_task(task, sleeptime, stop_event):
    while not stop_event.is_set():
        task()
        time.sleep(sleeptime)

def configure_components():
    """
    Configura los componentes IoT según los valores de habilitación.
    """
    return {
        "street_light": StreetLight(pir_led_pin=22, pir_sensor_pin=18, photo_led_pin=27, threshold=128) if IOT_INIT["ENABLE_STREET_LIGHT"] else None,
        "toll": Toll(toll_pin=23) if IOT_INIT["ENABLE_TOLL"] else None,
        "crane": Crane(pin_ultrasound_trig=16, pin_ultrasound_echo=26) if IOT_INIT["ENABLE_CRANE"] else None,
        "weather_station": WeatherStation(pin_weatherSensor=17, sleeptime=SLEEPTIME) if IOT_INIT["ENABLE_WEATHER_STATION"] else None,
        "railroad_switch": RailroadSwitch(pin_switch=20, pin_servo=21) if IOT_INIT["ENABLE_RAILROAD_SWITCH"] else None,
        "radar": Radar(pin_button=19) if IOT_INIT["ENABLE_RADAR"] else None,
    }

def start_IOT_Components():
    """
    Inicia los componentes IoT.
    """
    global components, threads, stop_event

    components = configure_components()
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


def stop_IOT_Components():
    """
    Stops IoT components.
    """
    global threads, stop_event

    stop_event.set()
    for thread in threads:
        thread.join()
    threads = []


# def stop_IOT_Components():
#     """
#     Detiene los componentes IoT.
#     """
#     global threads, stop_event

#     stop_event.set()
#     for thread in threads:
#         thread.join()
#     threads = []

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
# Rutas de control
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
@app.route('/start', methods=['POST'])
def start_components():
    global mode
    if mode == "running":
        return jsonify({"status": "error", "message": "Components already running"}), 400

    start_IOT_Components()
    mode = "running"
    print("Components started.")
    return jsonify({"status": "success", "message": "Components started"}), 200

@app.route('/stop', methods=['POST'])
def stop_components():
    global mode
    if mode == "stopped":
        return jsonify({"status": "error", "message": "Components already stopped"}), 400

    stop_IOT_Components()
    mode = "stopped"
    print("Components stopped.")
    return jsonify({"status": "success", "message": "Components stopped"}), 200

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "success", "state": mode}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
# Rutas de IOT
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
@app.route('/ledDetectionActuator', methods=['POST'])
def led_detection_actuator():
    if mode == "stopped":
        return jsonify({"status": "error", "message": "IoT components are stopped"}), 500
    if components["street_light"] is None:
        return jsonify({"status": "error", "message": "Street Light component is not enabled"}), 500
    try:
        data = request.json.get("data")[0]
        # print(f"Received data for LED Detection Actuator: {data}")
        led_state = data.get("presence", {}).get("value")
        # print(led_state)
        components["street_light"].control_lights_server_led(led_state)
        return jsonify({"status": "success", "data": data}), 201
    except Exception as e:
        print(f"Error handling LED Detection Actuator: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/lightActuator', methods=['POST'])
def light_actuator():
    if mode == "stopped":
        return jsonify({"status": "error", "message": "IoT components are stopped"}), 500
    if components["street_light"] is None:
        return jsonify({"status": "error", "message": "Street Light component is not enabled"}), 500
    try:
        data = request.json.get("data")[0] 
        sensor = data.get("id")
        print(sensor)
        if sensor == 'urn:ngsi-ld:PirSensor:001':
            print(f"Received data for Light Actuator: {data}")
            led_state = data.get("presence", {}).get("value")
            print(led_state)
            components["street_light"].control_lights_server_light_state(led_state)
        elif sensor == 'urn:ngsi-ld:PhotoresistorSensor:001':
            # Received data for Photoresistor Sensor: {'id': 'urn:ngsi-ld:PhotoresistorSensor:001', 'type': 'PhotoresistorSensor', 'light': {'type': 'Property', 'value': 0.905882}}
            print(f"Received data for ###Photoresistor### Sensor: {data}")
            intesity= data.get("light", {}).get("value")
            print(intesity)
            print("dasdasdfasdfasdf")
            # print(intesity)
            # print("dasdasdfasdfasdf")
            components["street_light"].control_lights_server_light(intesity)
        else:
            print('Nothing')
        return jsonify({"status": "success", "data": data}), 201
    except Exception as e:
        print(f"Error handling Light Actuator: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Camera
@app.route('/cameraActuator', methods=['POST'])
def camera_actuator():
    if mode == "stopped":
        return jsonify({"status": "error", "message": "IoT components are stopped"}), 500
    if components["radar"] is None:
        return jsonify({"status": "error", "message": "Radar component is not enabled"}), 500
    try:
        data = request.json.get("data")[0]
        print(f"Received data for Camera Actuator: {data}")
        presence = data.get("presence", {}).get("value")
#                 led_state = data.get("presence", {}).get("value")
        components["radar"].control_camera_server(presence)
        return jsonify({"status": "success", "data": data}), 201
    except Exception as e:
        print(f"Error handling Camera Actuator: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
# Received data for Camera Actuator: {'id': 'urn:ngsi-ld:InfraredSensor:001', 'type': 'InfraredSensor', 'presence': {'type': 'Property', 'value': True}}


# Servmotor
@app.route('/servmotorActuator', methods=['POST'])
def servmotor_actuator():
    if mode == "stopped":
        return jsonify({"status": "error", "message": "IoT components are stopped"}), 500
    if components["railroad_switch"] is None:
        return jsonify({"status": "error", "message": "Railroad Switch component is not enabled"}),
    try:
        data = request.json.get("data")[0]
        print(f"Received data for Servomotor Actuator: {data}")
        # result = self.servmotor_change(data.get("stateMotor"))
        # return jsonify(result), 201
        state_value = data.get("state", {}).get("value")
        print(state_value)
        components["railroad_switch"].control_servo_server(state_value)
        return jsonify({"status": "success", "data": data}), 201
    except Exception as e:
        print(f"Error handling Servomotor Actuator: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Train 
# @app.route('/engineDCActuator', methods=['POST'])
# def engine_dc_actuator():
#     if mode == "stopped":
#         return jsonify({"status": "error", "message": "IoT components are stopped"}), 500
#     print('Engine DC Actuator, no configurado')
    # try:
    #     data = request.json.get("data")[0]
    #     print(f"Received data for Engine DC Actuator: {data}")
    #     # result = self.engine_dc_change(data.get("velocityEngine"))
    #     # return jsonify(result), 201
    #     return jsonify({"status": "success", "data": data}), 201    
    # except Exception as e:
    #     print(f"Error handling Engine DC Actuator: {e}")
    #     return jsonify({"status": "error", "message": str(e)}), 500



# 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)