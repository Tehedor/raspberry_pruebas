import time
import threading
from dotenv import load_dotenv

from server.server_iot import IoTServer

from components.streetlight import StreetLight
from components.toll.toll import Toll
from components.crane import Crane
from components.weatherStation import WeatherStation
# from components.weatherStation import DHT as WeatherStation
from components.railroadSwitch import RailroadSwitch
from components.radar import Radar

load_dotenv() # Load environment variables from .env file   

def sensor_task(task, sleeptime, stop_event):
    while not stop_event.is_set():
        task()
        time.sleep(sleeptime)


def main():
    sleeptime = 0.05
    
    # Config server 
    enable_server = False
    # port = None
    # host = None
    # server = IoTServer(host=host, port=port) if enable_server else None
    
    # Config components
    enable_street_light = True
    enable_toll = False             # va
    enable_crane = True
    enable_weather_station = False
    enable_railroad_switch = False  # va
    enable_radar = False
    enable_train = False
    
    street_light = StreetLight(pir_led_pin=22, pir_sensor_pin=18, photo_led_pin=27, threshold=128) if enable_street_light else None
    toll = Toll(toll_pin=23) if enable_toll else None
    crane = Crane(pin_ultrasound_trig=16, pin_ultrasound_echo=26) if enable_crane else None
    railroad_switch = RailroadSwitch(pin_switch=20, pin_servo=21) if enable_railroad_switch else None
    radar = Radar(pin_button=19) if enable_radar else None
    weather_station = WeatherStation(pin_weatherSensor=17, sleeptime=sleeptime) if enable_weather_station else None   # Tienes que poner pin 11 auque por alguna razon corresponde al pin 17, sino no funciona 
    # weather_station = WeatherStation(pin_weatherSensor=11) if enable_weather_station else None   # Tienes que poner pin 11 auque por alguna razon corresponde al pin 17, sino no funciona 
    
    # train = Train() if enable_train else None
    
    server = IoTServer(
        street_light=street_light,
        toll=toll,
        crane=crane,
        weather_station=weather_station,
        railroad_switch=railroad_switch,
        radar=radar,
        # train=train
    ) if enable_server else None
    
    # Crear una lista de funciones a ejecutar
    tasks = []
    if enable_server:
        tasks.append(server.run)
    if enable_street_light:
        if enable_server:
            tasks.append(street_light.control_lights_server)
        else:
            tasks.append(street_light.control_lights)
    if enable_toll:
        if enable_server:
            tasks.append(toll.read_card_server) 
        else:  
            tasks.append(toll.read_card)
    if enable_crane:
        if enable_server:
            tasks.append(crane.detect_distance_server)
        else:   
            tasks.append(crane.print_distance)
    if enable_weather_station:
        # tasks.append(weather_station.read_sensor)
        # tasks.append(weather_station.printResult)
        if enable_server:
            tasks.append(weather_station.detect_temperature_server)
        else:
            tasks.append(weather_station.printResult)
    if enable_radar:
        if enable_server:
            tasks.append(radar.control_button_server)
        else:
            tasks.append(radar.control_button)
    if enable_railroad_switch:
        if enable_server:
            tasks.append(railroad_switch.control_switch_server)
        else:
            tasks.append(railroad_switch.control_switch)
    # if enable_train:
    #     if enable_server:
    #         tasks.append(train.some_method_server)
    #     else:
    #         tasks.append(train.some_method)
    
    # # Crear y lanzar un hilo para cada tarea
    # stop_event = threading.Event()
    # threads = []
    # for task in tasks:
    #     thread = threading.Thread(target=sensor_task, args=(task, sleeptime))
    #     thread.start()
    #     threads.append(thread)
        
    # Crear y lanzar un hilo para cada tarea
    stop_event = threading.Event()
    threads = []
    for task in tasks:
        thread = threading.Thread(target=sensor_task, args=(task, sleeptime, stop_event))
        thread.start()
        threads.append(thread)
    
    
    
    try:
        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()
    
    # try:
    #     while True:
    #         for task in tasks:
    #             task()
    #         time.sleep(sleeptime)
    
    except KeyboardInterrupt:
        stop_event.set()
        # Destruir los objetos en caso de interrupción
        if enable_street_light:
            street_light.destroy()
        if enable_toll:
            toll.destroy()
        if enable_crane:
            crane.destroy()
        if enable_weather_station:
            weather_station.destroy()
        # if enable_train:
        #     train.destroy()
        if enable_radar:
            radar.destroy()
        if enable_railroad_switch:
            railroad_switch.destroy()
        print("Ending program")

if __name__ == '__main__':
    print('Program is starting...')
    main()