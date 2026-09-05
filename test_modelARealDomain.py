import pytest
from task15_modelARealDomain import get_sensor, add_measurement, add_sensor, Machine, Measurement, Sensor
from datetime import datetime

def test_add_sensor():
    machine = Machine("001M", "machine1")
    sensor = Sensor("001S", "sensor1")
    add_sensor(machine, sensor)
    assert machine.sensors[0] == sensor

def test_add_measurement():
    sensor = Sensor("001S", "sensor1")
    measurement = Measurement(32.2, "C", datetime.fromtimestamp(1887639468))
    add_measurement(sensor, measurement)
    assert sensor.measurements[0] == measurement

def test_get_sensor():
    machine = Machine("001M", "machine1")
    sensor = Sensor("001S", "sensor1")
    add_sensor(machine, sensor)
    assert get_sensor(machine, "001S") == sensor

def test_default_mutable():
    machine1 = Machine("001M", "machine1")
    sensor = Sensor("001S", "sensor1")
    machine2 = Machine("002M", "machine2")
    add_sensor(machine1, sensor)
    assert len(machine1.sensors) == 1
    assert len(machine2.sensors) == 0


