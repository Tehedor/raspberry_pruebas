import time
import threading
from dotenv import load_dotenv

from server.server_iot import IoTServer
from components.streetlight import StreetLight
from components.toll.toll import Toll
from components.crane import Crane
from components.weatherStation import WeatherStation
from components.railroadSwitch import RailroadSwitch
from components.radar import Radar

load_dotenv()  # Cargar variables de entorno del archivo .env

def sensor_task(task, sleeptime, stop_event):
    """
    Ejecuta una tarea en bucle hasta que se active un evento de detención.
    """
    while not stop_event.is_set():
        task()
        time.sleep(sleeptime)

def configure_iot_components():
    """
    Configura los componentes IoT según los valores de habilitación.
    """
    sleeptime = 0.05

    # Configurar los componentes habilitados
    enable_street_light = True
    enable_toll = False
    enable_crane = False
    enable_weather_station = False
    enable_railroad_switch = False
    enable_radar = True

    components = {
        "street_light": StreetLight(pir_led_pin=22, pir_sensor_pin=18, photo_led_pin=27, threshold=128) if enable_street_light else None,
        "toll": Toll(toll_pin=23) if enable_toll else None,
        "crane": Crane(pin_ultrasound_trig=16, pin_ultrasound_echo=26) if enable_crane else None,
        "weather_station": WeatherStation(pin_weatherSensor=17, sleeptime=sleeptime) if enable_weather_station else None,
        "railroad_switch": RailroadSwitch(pin_switch=20, pin_servo=21) if enable_railroad_switch else None,
        "radar": Radar(pin_button=19) if enable_radar else None,
    }

    server = IoTServer(**components) if True else None 

    return components, server, sleeptime

def run_iot():
    """
    Inicializa y ejecuta las tareas IoT.
    """
    components, server, sleeptime = configure_iot_components()

    # Configurar tareas
    tasks = []
    stop_event = threading.Event()

    if server:
        tasks.append(server.run)
    if components["street_light"]:
        tasks.append(components["street_light"].control_lights_server if server else components["street_light"].control_lights)
    if components["toll"]:
        tasks.append(components["toll"].read_card_server if server else components["toll"].read_card)
    if components["crane"]:
        tasks.append(components["crane"].detect_distance_server if server else components["crane"].print_distance)
    if components["weather_station"]:
        tasks.append(components["weather_station"].detect_temperature_server if server else components["weather_station"].printResult)
    if components["radar"]:
        tasks.append(components["radar"].control_button_server if server else components["radar"].control_button)
    if components["railroad_switch"]:
        tasks.append(components["railroad_switch"].control_switch_server if server else components["railroad_switch"].control_switch)

    # Ejecutar las tareas en hilos
    threads = []
    for task in tasks:
        thread = threading.Thread(target=sensor_task, args=(task, sleeptime, stop_event))
        thread.start()
        threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        stop_event.set()
        destroy_components(components)

def destroy_components(components):
    """
    Destruye los componentes habilitados.
    """
    for name, component in components.items():
        if component:
            component.destroy()
    print("Componentes destruidos correctamente.")

if __name__ == '__main__':
    print('El programa está iniciándose...')
    run_iot()
