from task13_replaceDictionarywithDataModel import normalize_sensor_data
def validate_sensor_data(data):
    if not isinstance(data, dict):
        return False, "data is not dictionary type"

    if not "sensor" in data or not "value" in data or not "unit" in data:
        return False, "missing a property"

    if not data["sensor"] in ["EngineTemp", "engine_temperature", "ENGINE-TEMP"]:
        return False, "wrong sensor name"

    try:
        float(data["value"])
    except ValueError:
        return False, "value error in value"
    except TypeError:
        return False, "type error in value"

    if not data["unit"] in ["C", "F"]:
        return False, "invalid unit"

    return True, "data format is correct"

def process_sensor_batch(datasets):
    processed_datasets = {
        "successful": [],
        "failed": []
    }
    for data in datasets:
        validation, message = validate_sensor_data(data)
        if validation:
            normalized_data = normalize_sensor_data(data)
            processed_datasets["successful"].append(normalized_data)
        else:
            new_failed_data = {}
            new_failed_data["data"] = data
            new_failed_data["error"] = message
            processed_datasets["failed"].append(new_failed_data)

    return processed_datasets

if __name__ == "__main__":
    datasets = [
    {
        "sensor": "EngineTemp",
        "value": "85.4",
        "unit": "C"
    },
    {
        "sensor": "engine_temperature",
        "value": 185.72,
        "unit": "F"
    },
    {
        "sensor": "ENGINE-TEMP",
        "value": "85.7",
        "unit": "C"
    },
    {
        "sensor": "EngineTemp",
        "value": "hello",
        "unit": "C"
    },
    {
        "sensor": "EngineTemp",
        "value": 100,
        "unit": "K"
    }
]
    print(process_sensor_batch(datasets))




