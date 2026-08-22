from dataclasses import dataclass
from typing import TypedDict

@dataclass
class RawSensorData(TypedDict):
    sensor: str
    value: str | float
    unit: str

@dataclass
class SensorData:
    sensor: str
    value: float
    unit: str

def normalize_sensor_name(original_name:str) -> str:
    if original_name in ["EngineTemp", "engine_temperature", "ENGINE-TEMP"]:
        name = "engine_temperature"
    else:
        raise ValueError("wrong name")

    return name

def convert_temperature(original_temp: str | float, unit:str) -> float:
    float_temp = float(original_temp)

    if unit == "C":
        return float_temp
    elif unit == "F":
        return (float_temp - 32) * 5 / 9
    else:
        raise ValueError("wrong unit of temperature")

def normalize_sensor_data(data:RawSensorData) -> SensorData:
    sensor=normalize_sensor_name(data["sensor"])
    value = convert_temperature(data["value"], data["unit"])
    unit = "C"
    new_data = SensorData(sensor, value, unit)
    return new_data


if __name__ == "__main__":
    original_data = {
        "sensor": "EngineTemp",
        "value": "85.4",
        "unit": "C"
    }
    new_data = normalize_sensor_data(original_data)
    print(new_data.sensor, new_data.value, new_data.unit)

    

    
