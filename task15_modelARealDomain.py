from dataclasses import dataclass
from datetime import datetime

@dataclass
class Measurement:
    value: float
    unit: str
    timestamp: datetime

@dataclass
class Sensor:
    id: str
    name: str
    measurements: list[Measurement]

@dataclass
class Machine:
    id: str
    name: str
    sensors: list[Sensor]

def add_sensor(machine: Machine, sensor: Sensor) -> None:
    machine.sensors.append(sensor)
    return

def add_measurement(sensor: Sensor, measurement: Measurement) -> None:
    sensor.measurements.append(measurement)
    return

def get_sensor(machine: Machine, sensor_id: str) -> Sensor | None:
    for sensor in machine.sensors:
        if sensor.id == sensor_id:
            return sensor
    return None