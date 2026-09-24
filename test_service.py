from task15_modelARealDomain import Machine
from task27_repository import MachineRepository, SensorRepository, MeasurementRepository
import pytest
from datetime import datetime
from task18_databaseModeling import (create_connection, create_table)
from task28_service import MachineService


@pytest.fixture
def db_conn():
    conn = create_connection()
    create_table(conn)
    yield conn
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sensors;")
    cursor.execute("DELETE FROM machines;")
    conn.commit()
    conn.close()

def test_machine_exists_one_temperature_sensor(db_conn):
    machine_repo = MachineRepository(db_conn)
    sensor_repo = SensorRepository(db_conn)
    measurement_repo = MeasurementRepository(db_conn)

    machine_repo.add("MachineA")
    sensor_repo.add("Temperature", 1)
    measurement_repo.add(30, "C", 1, "2026-09-10 10:00:00")
    measurement_repo.add(34, "C", 1, "2026-09-10 10:00:00")

    service = MachineService(machine_repo, sensor_repo, measurement_repo)
    average = service.get_average_temperature("1")
    assert average == 32

def test_machine_exists_multiple_temperature_sensors(db_conn):
    machine_repo = MachineRepository(db_conn)
    sensor_repo = SensorRepository(db_conn)
    measurement_repo = MeasurementRepository(db_conn)

    machine_repo.add("MachineA")
    sensor_repo.add("Temperature", 1)
    sensor_repo.add("Temperature", 1)
    measurement_repo.add(30, "C", 1, "2026-09-10 10:00:00")
    measurement_repo.add(34, "C", 1, "2026-09-10 10:00:00")
    measurement_repo.add(33, "C", 2, "2026-09-10 10:00:00")
    measurement_repo.add(35, "C", 2, "2026-09-10 10:00:00")

    service = MachineService(machine_repo, sensor_repo, measurement_repo)
    average = service.get_average_temperature("1")
    assert average == 33

def test_machine_doesnt_exist(db_conn):
    machine_repo = MachineRepository(db_conn)
    sensor_repo = SensorRepository(db_conn)
    measurement_repo = MeasurementRepository(db_conn)
    service = MachineService(machine_repo, sensor_repo, measurement_repo)
    average = service.get_average_temperature("1")
    assert average is None

def test_temperature_sensor_exists_but_no_measurements(db_conn):
    machine_repo = MachineRepository(db_conn)
    sensor_repo = SensorRepository(db_conn)
    measurement_repo = MeasurementRepository(db_conn)

    machine_repo.add("MachineA")
    sensor_repo.add("Temperature", 1)
    sensor_repo.add("Temperature", 1)

    service = MachineService(machine_repo, sensor_repo, measurement_repo)
    average = service.get_average_temperature("1")
    assert average is None

def test_machine_has_no_temperate_sensor(db_conn):
    machine_repo = MachineRepository(db_conn)
    sensor_repo = SensorRepository(db_conn)
    measurement_repo = MeasurementRepository(db_conn)

    machine_repo.add("MachineA")
    sensor_repo.add("Pressure", 1)
    measurement_repo.add(30, "P", 1, "2026-09-10 10:00:00")
    measurement_repo.add(34, "P", 1, "2026-09-10 10:00:00")

    service = MachineService(machine_repo, sensor_repo, measurement_repo)
    average = service.get_average_temperature("1")
    assert average is None

