from datetime import datetime
import pytest
from task18_databaseModeling import (insert_machine, insert_measurement, insert_sensor,
                                     find_machine_by_id, find_sensor_by_id, get_measurements_for_sensor,
                                     get_complete_machines, create_connection, create_table)
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

def setup_test_data(db_conn):
    # Machines
    insert_machine(db_conn, "MachineA")  # id = 1
    insert_machine(db_conn, "MachineB")  # id = 2

    # Sensors
    insert_sensor(db_conn, "Temperature", 1)  # sensor id = 1
    insert_sensor(db_conn, "Pressure", 1)     # sensor id = 2
    insert_sensor(db_conn, "Temperature", 2)  # sensor id = 3

    # Measurements
    insert_measurement(
        db_conn, 33.4, "C", 1,
        # datetime.strptime("2026-09-10 10:00:00", "%Y-%m-%d %H:%M:%S")
        "2026-09-10 10:00:00"
    )

    insert_measurement(
        db_conn, 34.1, "C", 1,
        # datetime.strptime("2026-09-10 11:00:00", "%Y-%m-%d %H:%M:%S")
        "2026-09-10 11:00:00"
    )

    insert_measurement(
        db_conn, 100, "P", 2,
        # datetime.strptime("2026-09-10 10:00:00", "%Y-%m-%d %H:%M:%S")
        "2026-09-10 11:00:00"
    )

    insert_measurement(
        db_conn, 29.7, "C", 3,
        # datetime.strptime("2026-09-10 10:00:00", "%Y-%m-%d %H:%M:%S")
        "2026-09-10 11:00:00"
    )

def test_find_existing_machine(db_conn):
    setup_test_data(db_conn)
    machines = get_complete_machines(db_conn)
    machine = find_machine_by_id(machines, "1")
    assert machine.name == "MachineA"

def test_machine_does_not_exist(db_conn):
    setup_test_data(db_conn)
    machines = get_complete_machines(db_conn)
    machine = find_machine_by_id(machines, "A")
    assert machine is None

def test_find_existing_sensor(db_conn):
    setup_test_data(db_conn)
    machines = get_complete_machines(db_conn)
    sensor = find_sensor_by_id(machines, "1")
    assert sensor.name == "Temperature"

def test_sensor_doesnt_exist(db_conn):
    setup_test_data(db_conn)
    machines = get_complete_machines(db_conn)
    sensor = find_sensor_by_id(machines, "100")
    assert sensor is None

def test_get_measurement_for_sensor(db_conn):
    setup_test_data(db_conn)
    machines = get_complete_machines(db_conn)
    measurements = get_measurements_for_sensor(machines, "1")
    assert len(measurements) == 2
    assert measurements[0].value == 33.4
    assert measurements[1].value == 34.1

def test_sensor_exist_no_measurement(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Pressure", 1)
    machines = get_complete_machines(db_conn)
    measurements = get_measurements_for_sensor(machines, "1")
    assert measurements == []

def test_get_measurements_for_nonexistent_sensor(db_conn):
    setup_test_data(db_conn)
    machines = get_complete_machines(db_conn)
    measurements = get_measurements_for_sensor(machines, "500")
    assert measurements == []