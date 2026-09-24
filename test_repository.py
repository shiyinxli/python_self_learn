from task18_databaseModeling import (create_table, create_connection, get_machines, insert_machine, row_to_machine, get_machine_objects, insert_sensor, get_sensor_objects, get_machines_with_sensors, insert_measurement, get_measurement_objects, 
                                     get_complete_machines, get_average_for_sensor, get_highest_measurement_for_sensor, find_sensors_by_name, get_average_for_sensor_name)
                                     
from task15_modelARealDomain import Machine
from task27_repository import MachineRepository
import pytest
from datetime import datetime


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

def test_repository_can_be_created(db_conn):
    repo = MachineRepository(db_conn)
    assert repo is not None

def test_add_a_machine(db_conn):
    repo = MachineRepository(db_conn)
    repo.add("MachineA")
    machine = repo.get_by_id("1")
    assert machine.name == "MachineA"

def test_get_all_returns_all_machines(db_conn):
    repo = MachineRepository(db_conn)
    repo.add("MachineA")
    repo.add("MachineB")
    machines = repo.get_all()
    assert len(machines) == 2

def test_get_all_returns_empty(db_conn):
    repo = MachineRepository(db_conn)
    machines = repo.get_all()
    assert machines == []

def test_get_by_id_finds_an_existing_machine(db_conn):
    repo = MachineRepository(db_conn)
    repo.add("MachineA")
    machine = repo.get_by_id("1")
    assert machine.name == "MachineA"

def test_returns_none_for_nonexistent_machine(db_conn):
    repo = MachineRepository(db_conn)
    repo.add("MachineA")
    machine = repo.get_by_id("4")
    assert machine is None

