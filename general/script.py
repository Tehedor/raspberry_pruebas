import time
import threading

from components.streetlight import StreetLight
from components.toll.toll import Toll
from components.crane import Crane

# from components.weatherStation.weatherStation import WeatherStation
from components.weatherStation.Freenove_DHT import DHT as WeatherStation

from components.railroadSwitch import RailroadSwitch
# from components.train import Train
from components.radar import Radar

def sensor_task(task, sleeptime, stop_event):
    while not stop_event.is_set():
        task()
        time.sleep(sleeptime)


def main():
    enable_street_light = False
    enable_toll = False
    enable_crane = False
    enable_weather_station = False
    enable_railroad_switch = False
    enable_train = False
    enable_radar = True
    
    sleeptime = 0.05
    
    # Crear instancias de los componentes según la configuración
    street_light = StreetLight(pir_led_pin=22, pir_sensor_pin=18, photo_led_pin=27, threshold=128) if enable_street_light else None
    toll = Toll(toll_pin=23) if enable_toll else None
    crane = Crane(pin_ultrasound_trig=16, pin_ultrasound_echo=26) if enable_crane else None
    railroad_switch = RailroadSwitch(pin_switch=20, pin_servo=21) if enable_railroad_switch else None
    radar = Radar(pin_button=19) if enable_radar else None
    
    # weather_station = WeatherStation(pin_weatherSensor=11) if enable_weather_station else None   # Tienes que poner pin 11 auque por alguna razon corresponde al pin 17, sino no funciona 
    weather_station = WeatherStation(pin_weatherSensor=11, sleeptime=sleeptime) if enable_weather_station else None   # Tienes que poner pin 11 auque por alguna razon corresponde al pin 17, sino no funciona 
    
    train = Train() if enable_train else None
    
    # Crear una lista de funciones a ejecutar
    tasks = []
    if enable_street_light:
        tasks.append(street_light.control_lights)
    if enable_toll:
        tasks.append(toll.read_card)
    if enable_crane:
        tasks.append(crane.print_distance)
    if enable_weather_station:
        # tasks.append(weather_station.read_sensor)
        tasks.append(weather_station.printResult)
    if enable_train:
        tasks.append(train.some_method)  # Reemplaza some_method con el método adecuado
    if enable_radar:
        tasks.append(radar.control_button)  # Reemplaza some_method con el método adecuado
    if enable_railroad_switch:
        tasks.append(railroad_switch.control_switch)  # Reemplaza some_method con el método adecuado
    
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
        if enable_train:
            train.destroy()
        if enable_radar:
            radar.destroy()
        if enable_railroad_switch:
            railroad_switch.destroy()
        print("Ending program")

if __name__ == '__main__':
    print('Program is starting...')
    main()