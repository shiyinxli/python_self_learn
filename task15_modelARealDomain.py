from dataclasses import dataclass, field
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
    measurements: list[Measurement] = field(default_factory = list)

@dataclass
class Machine:
    id: str
    name: str
    sensors: list[Sensor] = field(default_factory=list)

def add_sensor(machine: Machine, sensor: Sensor) -> None:
    machine.sensors.append(sensor)

def add_measurement(sensor: Sensor, measurement: Measurement) -> None:
    sensor.measurements.append(measurement)

def get_sensor(machine: Machine, sensor_id: str) -> Sensor | None:
    for sensor in machine.sensors:
        if sensor.id == sensor_id:
            return sensor
    return None