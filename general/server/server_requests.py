# from flask import request
import requests as request

IP_server = '138.4.22.12'
# BASE_URL = f'http://{IP_server}:1026/ngsi-ld/v1/entities'
# http://138.4.22.12:80/orion/ngsi-ld/v1/entities
BASE_URL = f'http://{IP_server}:80/orion/ngsi-ld/v1/entities'
HEADERS = {
    'Content-Type': 'application/json',
    'Link': '<http://context/datamodels.context-ngsi.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
}

def patch_entity(entity_id, attribute, value):
    url = f"{BASE_URL}/{entity_id}/attrs"
    payload = {attribute: value}
    response = request.patch(url, json=payload, headers=HEADERS)
    return response.json() if response.ok else {"error": "PATCH failed"}


# Streetlight
def pir_sensor_change(presence):
    entity_id = f"urn:ngsi-ld:PirSensor:001"
    return patch_entity(entity_id, "presence", presence)

def led_detection_change(state_led):
    entity_id = f"urn:ngsi-ld:LedDetection:001"
    return patch_entity(entity_id, "stateLed", state_led)

def photoresistor_sensor_change(intensity):
    entity_id = f"urn:ngsi-ld:PhotoresistorSensor:001"
    return patch_entity(entity_id, "light", intensity)

def light_change(state_light):
    entity_id = f"urn:ngsi-ld:Light:001"
    return patch_entity(entity_id, "stateLight", state_light)

# Trainled_detection_change
def potentiometer_sensor_change(velocity_control):
    entity_id = f"urn:ngsi-ld:PotentiometerSensor:001"
    return patch_entity(entity_id, "velocityControl", velocity_control)

def engine_dc_change(velocity):
    entity_id = f"urn:ngsi-ld:EngineDC:001"
    return patch_entity(entity_id, "velocityEngine", velocity)

# RailroadSwitch
def switch_sensor_change(state):
    entity_id = f"urn:ngsi-ld:SwitchSensor:001"
    return patch_entity(entity_id, "state", state)

def servmotor_change(state_motor):
    entity_id = f"urn:ngsi-ld:Servmotor:001"
    return patch_entity(entity_id, "stateMotor", state_motor)

# Radar
def infrared_sensor_change(presence):
    entity_id = f"urn:ngsi-ld:InfraredSensor:001"
    return patch_entity(entity_id, "presence", presence)

def camera_change(state_camera, media_url):
    entity_id = f"urn:ngsi-ld:Camera:001"
    return patch_entity(entity_id, "stateCamera", state_camera)

# Crane
def ultrasound_sensor_change(distance):
    entity_id = f"urn:ngsi-ld:UltrasoundSensor:001"
    payload = {
        "distance": {
            "type": "Property",
            "value": distance,
            "unitCode": "CMT"
        }
    }
    return patch_entity(entity_id, "distance", payload)

# WheaterStation
def temperature_sensor_change(temperature):
    entity_id = f"urn:ngsi-ld:TemperatureSensor:001"
    payload = {
        "temperature": {
            "type": "Property",
            "value": temperature,
            "unitCode": "CEL"
        }
    }
    return patch_entity(entity_id, "temperature", payload)

def humidity_sensor_change(humidity):
    entity_id = f"urn:ngsi-ld:HumiditySensor:001"
    payload = {
        "humidity": {
            "type": "Property",
            "value": humidity,
            "unitCode": "P1"
        }
    }
    return patch_entity(entity_id, "humidity", payload)

# Toll
def rfid_sensor_change(uid):
    entity_id = f"urn:ngsi-ld:RfidSensor:001"
    return patch_entity(entity_id, "uiddcode", uid)