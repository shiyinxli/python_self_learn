from task18_databaseModeling import (create_table, create_connection, get_machines, insert_machine, row_to_machine, get_machine_objects, insert_sensor, get_sensor_objects, get_machines_with_sensors, insert_measurement, get_measurement_objects, 
                                     get_complete_machines, get_average_for_sensor, get_highest_measurement_for_sensor, find_sensors_by_name, get_average_for_sensor_name)
                                     
from task15_modelARealDomain import Machine
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

def test_create_connection():
    conn = create_connection()
    assert conn is not None

def test_get_machines(db_conn):
    insert_machine(db_conn, "MachineA")
    rows = get_machines(db_conn)
    assert rows[0][1] == "MachineA"
    assert len(rows) == 1

def test_empty_database(db_conn):
    rows = get_machines(db_conn)
    assert rows == []

def test_multiple_machines(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_machine(db_conn, "MachineB")
    rows = get_machines(db_conn)
    assert len(rows) == 2
    assert rows[0][1] == "MachineA"
    assert rows[1][1] == "MachineB"


def test_raw_conversion():
    row = (5, "MachineX")
    machine = row_to_machine(row)
    assert machine.id == "5"
    assert machine.name == "MachineX"
    assert machine.sensors == []

def test_multiple_database_record(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_machine(db_conn, "MachineB")
    machines = get_machine_objects(db_conn)
    assert len(machines) == 2
    assert isinstance(machines[0], Machine)
    assert isinstance(machines[1], Machine)   

def test_empty_database_object(db_conn):
    machines = get_machine_objects(db_conn)
    assert machines == []

def test_insert_one_sensor(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)
    sensors = get_sensor_objects(db_conn)
    sensor = sensors[0]
    assert len(sensors) == 1
    assert sensor.id == "1"
    assert sensor.name == "Temperature"
    assert sensor.measurements == []

def test_insert_multiple_sensors(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)
    insert_sensor(db_conn, "Pressure", 1)
    sensors = get_sensor_objects(db_conn)
    sensor1 = sensors[0]
    sensor2 = sensors[1]
    assert len(sensors) == 2
    assert sensor1.id == "1"
    assert sensor1.name == "Temperature"
    assert sensor1.measurements == []
    assert sensor2.id == "2"
    assert sensor2.name == "Pressure"
    assert sensor2.measurements == []

def test_empty_sensor_table(db_conn):
    sensors = get_sensor_objects(db_conn)
    assert sensors == []

def test_insert_sensor_invalid_machine_id(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 999)
    sensors = get_sensor_objects(db_conn)
    assert sensors == []

def test_get_machines_with_sensors_one_sensor(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1) 
    machines =  get_machines_with_sensors(db_conn)
    assert machines[0].sensors[0].name == "Temperature"
    assert len(machines[0].sensors) == 1 

def test_get_machines_with_multiple_sensors(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)
    insert_sensor(db_conn, "Pressure", 1)
    machines = get_machines_with_sensors(db_conn)
    assert len(machines[0].sensors) == 2
    assert machines[0].sensors[0].name == "Temperature"
    assert machines[0].sensors[1].name == "Pressure"

def test_get_machine_with_sensors_two_machines_with_different_sensors(db_conn):    
    insert_machine(db_conn, "MachineA")
    insert_machine(db_conn, "MachineB")
    insert_sensor(db_conn, "Temperature", 1)
    insert_sensor(db_conn, "Pressure", 1)
    insert_sensor(db_conn, "Temperature_", 2)
    insert_sensor(db_conn, "Pressure_", 2)

    machines = get_machines_with_sensors(db_conn)
    assert len(machines[0].sensors) == 2
    assert len(machines[1].sensors) == 2
    assert machines[0].sensors[0].name == "Temperature"
    assert machines[1].sensors[1].name == "Pressure_"

def test_get_machines_with_no_sensor(db_conn):
    insert_machine(db_conn, "MachineA")
    machines = get_machines_with_sensors(db_conn)
    assert len(machines[0].sensors) == 0

def test_get_machines_with_sensors_empty_database(db_conn):
    machines = get_machines_with_sensors(db_conn)
    assert len(machines) == 0

def test_insert_one_measurement(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00")
    measurements = get_measurement_objects(db_conn)
    assert len(measurements) == 1
    assert isinstance(measurements[0].timestamp, datetime)
    assert measurements[0].timestamp == datetime.strptime(
    "2026-09-10 10:00:00",
    "%Y-%m-%d %H:%M:%S"
)
    assert measurements[0].value == 33.4

def test_empty_measurement_table(db_conn):
    measurements = get_measurement_objects(db_conn)
    assert measurements == []

def test_invalid_sensorId_insert_measurements(db_conn):
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00")
    measurements = get_measurement_objects(db_conn)
    assert measurements == []

def test_insert_multiple_measurements(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00")
    insert_measurement(db_conn, 33.1, "C", 1, "2026-09-10 11:00:00")
    insert_measurement(db_conn, 35, "C", 1, "2026-09-10 10:00:00")
    measurements = get_measurement_objects(db_conn)
    assert len(measurements) == 3


def test_one_machine_one_sensor_one_measurement(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00")
    machines = get_complete_machines(db_conn)
    assert machines[0].sensors[0].measurements[0].value == 33.4

def test_one_machine_multiple_sensors_multiple_measurements(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1) 
    insert_sensor(db_conn, "Pressure", 1)   
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00")
    insert_measurement(db_conn, 100, "P", 2, "2026-09-10 12:00:00")
    machines = get_complete_machines(db_conn)
    assert machines[0].sensors[0].measurements[0].value == 33.4
    assert machines[0].sensors[1].measurements[0].value == 100

def test_two_machine_multiple_sensors_multiple_measurements(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_machine(db_conn, "MachineB")
    insert_sensor(db_conn, "Temperature", 1) 
    insert_sensor(db_conn, "Pressure", 2)   
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00")
    insert_measurement(db_conn, 100, "P", 2, "2026-09-10 12:00:00")
    machines = get_complete_machines(db_conn)
    assert machines[0].sensors[0].measurements[0].value == 33.4
    assert machines[1].sensors[0].measurements[0].value == 100

def test_sensor_with_no_measurements(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1) 
    insert_sensor(db_conn, "Pressure", 1)  
    machines = get_complete_machines(db_conn)
    assert not machines[0].sensors[0].measurements

def test_machine_with_no_sensors(db_conn):
    insert_machine(db_conn, "MachineA")
    machines = get_complete_machines(db_conn)
    assert not machines[0].sensors

def test_empty_machines(db_conn):
    machines = get_complete_machines(db_conn)
    assert not machines

def test_verify_actual_values_timestamps(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00") 
    machines = get_complete_machines(db_conn)
    assert machines[0].sensors[0].measurements[0].value == 33.4
    assert machines[0].sensors[0].measurements[0].timestamp == datetime.strptime(
        "2026-09-10 10:00:00",
        "%Y-%m-%d %H:%M:%S"
    )

def test_average_for_existing_sensor(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 32.4, "C", 1, "2026-09-10 10:00:00")
    insert_measurement(db_conn, 34.4, "C", 1, "2026-09-10 10:00:00") 
    machines = get_complete_machines(db_conn)
    average = get_average_for_sensor(machines, "1")
    assert average == 33.4

def test_average_for_nonexistent_sensor(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00") 
    machines = get_complete_machines(db_conn)
    average = get_average_for_sensor(machines, "5")
    assert average is None

def test_average_for_sensor_with_no_measurements(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    machines = get_complete_machines(db_conn)
    average = get_average_for_sensor(machines, "1")
    assert average is None

def test_highest_measurement_for_existing_sensor(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 32.4, "C", 1, "2026-09-10 10:00:00")
    insert_measurement(db_conn, 34.4, "C", 1, "2026-09-10 10:00:00") 
    machines = get_complete_machines(db_conn)
    highest = get_highest_measurement_for_sensor(machines, "1")
    assert highest.value == 34.4

def test_highest_for_nonexistent_sensor(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33.4, "C", 1, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 32.4, "C", 1, "2026-09-10 10:00:00")
    insert_measurement(db_conn, 34.4, "C", 1, "2026-09-10 10:00:00") 
    machines = get_complete_machines(db_conn)
    highest = get_highest_measurement_for_sensor(machines, "2")
    assert highest is None

def test_highest_for_sensors_with_no_measurements(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1) 
    machines = get_complete_machines(db_conn)
    highest = get_highest_measurement_for_sensor(machines, "1")
    assert highest is None 


def test_find_one_sensor_by_name(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33, "C", 1, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 35, "C", 1, "2026-09-10 10:00:00")  
    insert_machine(db_conn, "MachineB")
    insert_sensor(db_conn, "Temperature", 2)    
    insert_measurement(db_conn, 29, "C", 2, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 31, "C", 2, "2026-09-10 10:00:00")  
    machines = get_complete_machines(db_conn)
    sensors = find_sensors_by_name(machines, "Temperature")
    assert len(sensors) == 2
    assert sensors[0].name == "Temperature"
    assert sensors[1].id == "2"

def test_no_matching_sensor(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33, "C", 1, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 35, "C", 1, "2026-09-10 10:00:00")  
    insert_machine(db_conn, "MachineB")
    insert_sensor(db_conn, "Temperature", 2)    
    insert_measurement(db_conn, 29, "C", 2, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 31, "C", 2, "2026-09-10 10:00:00")  
    machines = get_complete_machines(db_conn)
    sensors = find_sensors_by_name(machines, "Pressure")
    assert sensors == []

def test_average_across_multiple_machines(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature",1)    
    insert_measurement(db_conn, 33, "C", 1, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 35, "C", 1, "2026-09-10 10:00:00")  
    insert_machine(db_conn, "MachineB")
    insert_sensor(db_conn, "Temperature", 2)    
    insert_measurement(db_conn, 29, "C", 2, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 31, "C", 2, "2026-09-10 10:00:00")  
    machines = get_complete_machines(db_conn)
    average = get_average_for_sensor_name(machines, "Temperature")
    assert len(machines) == 2
    assert machines[1].sensors[0].measurements[0].value == 29
    assert average == 32

def test_matching_sensors_but_no_measurements(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)   
    machines = get_complete_machines(db_conn)
    average = get_average_for_sensor_name(machines, "Temperature")
    assert average is None

def test_no_matching_sensor(db_conn):
    insert_machine(db_conn, "MachineA")
    insert_sensor(db_conn, "Temperature", 1)    
    insert_measurement(db_conn, 33, "C", 1, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 35, "C", 1, "2026-09-10 10:00:00")  
    insert_machine(db_conn, "MachineB")
    insert_sensor(db_conn, "Temperature", 2)    
    insert_measurement(db_conn, 29, "C", 2, "2026-09-10 10:00:00") 
    insert_measurement(db_conn, 31, "C", 2, "2026-09-10 10:00:00")  
    machines = get_complete_machines(db_conn)
    average = get_average_for_sensor_name(machines, "temperature")
    assert average is None




