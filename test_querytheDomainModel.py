import pytest
from task15_modelARealDomain import get_sensor, add_measurement, add_sensor, Machine, Measurement, Sensor
from datetime import datetime
from task17_querytheDomainModel import average_measurement, highest_measurement

def test_average_measurement_empty_sensor():
    sensor = Sensor("001S", "sensor1")
    assert average_measurement(sensor) is None

def test_average_measurement_one_measurement():
    sensor = Sensor("001S", "sensor1")
    measure = Measurement(33.2, "C", datetime.now())
    add_measurement(sensor, measure)
    assert average_measurement(sensor) == measure.value

def test_average_measurement_multi_measurements():
    sensor = Sensor("001S", "sensor1")
    measure1 = Measurement(85.0, "C", datetime.now())
    measure2 = Measurement(87.0, "C", datetime.now())
    measure3 = Measurement(88.0, "C", datetime.now())
    add_measurement(sensor, measure1)
    add_measurement(sensor, measure2)
    add_measurement(sensor, measure3)
    assert average_measurement(sensor) == pytest.approx(86.6, 0.1)

def test_highest_measurement_empty_sensor():
    sensor = Sensor("001S", "sensor1")
    assert  highest_measurement(sensor) is None

def test_highest_measurement_one_measurement():
    sensor = Sensor("001S", "sensor1")
    measure = Measurement(33.2, "C", datetime.now())
    add_measurement(sensor, measure)
    assert highest_measurement(sensor) == measure

def test_highest_measurement_multi_measurements():
    sensor = Sensor("001S", "sensor1")
    measure1 = Measurement(85.0, "C", datetime.now())
    measure2 = Measurement(92.0, "C", datetime.now())
    measure3 = Measurement(92.0, "C", datetime.now())
    add_measurement(sensor, measure1)
    add_measurement(sensor, measure2)
    add_measurement(sensor, measure3)
    assert highest_measurement(sensor) == measure2
