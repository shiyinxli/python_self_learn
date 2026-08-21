import pytest
from task11_processABatchOfSensorData import validate_sensor_data, process_sensor_batch

def test_valid_celciusData():
    validation, message = validate_sensor_data({
            "sensor": "EngineTemp",
            "value": "85.4",
            "unit": "C"
        })
    assert validation 
    assert message == "data format is correct"

def test_invalid_unit():
    validation, message = validate_sensor_data({
    "sensor": "EngineTemp",
    "value": "85.4",
    "unit": "K"
})
    assert not validation
    assert message == "invalid unit"

def test_invalid_string_value():
    validation, message = validate_sensor_data({
    "sensor": "EngineTemp",
    "value": "hello",
    "unit": "C"
})
    assert not validation
    assert message == "value error in value"

def test_none_value():
    validation, message = validate_sensor_data({
    "sensor": "EngineTemp",
    "value": None,
    "unit": "C"
})
    assert not validation
    assert message == "type error in value"

def test_process_sensor_batch():
    result = process_sensor_batch(datasets = [
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
        "sensor": "EngineTemp",
        "value": "hello",
        "unit": "C"
    },
    {
        "sensor": "EngineTemp",
        "value": 100,
        "unit": "K"
    }
])
    assert len(result["successful"]) == 2
    assert len(result["failed"]) == 2
    assert result["successful"][1]["sensor"] == "engine_temperature"
    assert result["successful"][1]["value"] == pytest.approx(85.4, rel=1e-9, abs=1e-12)
    assert result["successful"][1]["unit"] == "C"



