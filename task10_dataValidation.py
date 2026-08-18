from task9_normalizeSensorData import normalize_sensor_data

def validate_sensor_data(data):
    if not isinstance(data, dict):
        return False

    if not "sensor" in data or not "value" in data or not "unit" in data:
        return False

    if not data["sensor"] in ["EngineTemp", "engine_temperature", "ENGINE-TEMP"]:
        return False

    try:
        float(data["value"])
    except ValueError:
        return False
    except TypeError:
        return False

    if not data["unit"] in ["C", "F"]:
        return False

    return True

if __name__ == "__main__":
    datasets = [
    {
    "sensor": "EngineTemp",
    "value": "85.4",
    "unit": "C"
},
    ["EngineTemp", "85.4", "C"],
    {
    "sensor": "EngineTemp",
    "value": "85.4"
},
    {
    "sensor": "EngineTemp",
    "value": None,
    "unit": "C"
}]
    for data in datasets:
        if validate_sensor_data(data):
            print(normalize_sensor_data(data))
    

