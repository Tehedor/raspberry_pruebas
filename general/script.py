import time

from components.streetlight import StreetLight
from components.toll.toll import Toll
from components.crane import Crane
from components.weatherStation.weatherStation import WheaterStation
# from components.train import Train
# from components.radar import Radar
# from components.railroadSwitch import RailroadSwitch

def main():
    enable_street_light = True
    enable_toll = True
    enable_crane = True
    enable_weather_station = True
    enable_train = False
    enable_radar = False
    enable_railroad_switch = False
    
    sleeptime = 0.05
    
    # Crear instancias de los componentes según la configuración
    street_light = StreetLight(pir_led_pin=22, pir_sensor_pin=18, photo_led_pin=27, threshold=128) if enable_street_light else None
    toll = Toll(toll_pin=23) if enable_toll else None
    crane = Crane(trigPin=16, echoPin=26) if enable_crane else None
    weather_station = WheaterStation(wheaterSensorPin=11) if enable_weather_station else None   # Tienes que poner pin 11 auque por alguna razon corresponde al pin 17, sino no funciona 
    
    train = Train() if enable_train else None
    radar = Radar() if enable_radar else None
    railroad_switch = RailroadSwitch() if enable_railroad_switch else None
    
    # Crear una lista de funciones a ejecutar
    tasks = []
    if enable_street_light:
        tasks.append(street_light.control_lights)
    if enable_toll:
        tasks.append(toll.read_card)
    if enable_crane:
        tasks.append(crane.print_distance)
    if enable_weather_station:
        tasks.append(weather_station.read_sensor)
    if enable_train:
        tasks.append(train.some_method)  # Reemplaza some_method con el método adecuado
    if enable_radar:
        tasks.append(radar.some_method)  # Reemplaza some_method con el método adecuado
    if enable_railroad_switch:
        tasks.append(railroad_switch.some_method)  # Reemplaza some_method con el método adecuado
    
    try:
        while True:
            for task in tasks:
                task()
            time.sleep(sleeptime)
    
    except KeyboardInterrupt:
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