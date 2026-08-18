def normalize_sensor_name(original_name):
    if original_name in ["EngineTemp", "engine_temperature", "ENGINE-TEMP"]:
        name = "engine_temperature"
    else:
        raise ValueError("wrong name")

    return name

def convert_temperature(original_temp, unit):
    float_temp = float(original_temp)

    if unit == "C":
        return float_temp
    elif unit == "F":
        return (float_temp - 32) * 5 / 9
    else:
        raise ValueError("wrong unit of temperature")

def normalize_sensor_data(data):
    new_data = {}
    new_data["sensor"]=normalize_sensor_name(data["sensor"])
    new_data["value"] = convert_temperature(data["value"], data["unit"])
    new_data["unit"] = "C"
    return new_data

if __name__ == "__main__":
    data1 = {
        "sensor": "EngineTemp",
        "value": "85.4",
        "unit": "C"
    }

    data2 = {
        "sensor": "engine_temperature",
        "value": 185.72,
        "unit": "F"
    }

    data3 = {
        "sensor": "ENGINE-TEMP",
        "value": "85.7",
        "unit": "C"
    }

    print(normalize_sensor_data(data1))
    print(normalize_sensor_data(data2))
    print(normalize_sensor_data(data3))

