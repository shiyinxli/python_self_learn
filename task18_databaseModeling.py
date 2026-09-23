import sqlite3
from sqlite3 import Error
from task15_modelARealDomain import Machine, Sensor, Measurement
from datetime import datetime

def create_connection():
    try:
        conn = sqlite3.connect(':memory:')
        # print(f"Connected to SQLite database: {db_file}")
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        """)
        print("Table 'machines' is ready.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            machine_id INTEGER NOT NULL,
            FOREIGN KEY (machine_id) REFERENCES machines(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        """)
        print("Table 'sensors' is ready.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value REAL,
            unit TEXT NOT NULL,
            sensor_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (sensor_id) REFERENCES sensors(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        """)
        print("Table 'measurements' is ready.")
    except Error as e:
        print(f"Error when creating tables: {e}")

def insert_machine(conn, name):
    if not isinstance(name, str) or not name.strip():
        print("Invalid name.")
        return
    try:
        sql_insert = "INSERT INTO machines (name) VALUES (?)"
        conn.execute(sql_insert, (name.strip(),))
        conn.commit()
        print(f"Machine '{name}' added successfully.")
    except Error as e:
        print(f"Error inserting machines: {e}")

def get_machines(conn):
    try:
        cursor = conn.execute("SELECT id, name FROM machines")
        rows = cursor.fetchall()
        if rows:
            return rows
        else:
            return []
    except Error as e:
        return []

def row_to_machine(row) -> Machine:
    machine_id = str(row[0])
    name = row[1]
    sensors = []
    machine = Machine(machine_id, name, sensors)
    return machine

def get_machine_objects(conn) -> list[Machine]:
    try:
        machines = []
        cursor = conn.execute("SELECT id, name FROM machines")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                machine = row_to_machine(row)
                machines.append(machine)
        return machines
    except Error as e:
        return machines
    
def insert_sensor(conn, name: str, machine_id: int):
    if not isinstance(name, str) or not name.strip() or not isinstance(machine_id, int):
        print("Invalid name or machine id")
        return
    cursor = conn.execute("SELECT id FROM machines")
    rows = cursor.fetchall()
    machine_ids = [row[0] for row in rows]
    if not machine_id in machine_ids:
        print("invalid machine id")
        return
    try:
        sql_insert = "INSERT INTO sensors (name, machine_id) VALUES (?,?)"
        conn.execute(sql_insert, (name.strip(), machine_id))
        conn.commit()
        print(f"Sensor '{name}' added successfully.")
    except Error as e:
        print(f"Error inserting sensors: {e}")

def row_to_sensor(row) -> Sensor:
    sensor_id = str(row[0])
    name = row[1]
    machine_id = str(row[2])
    measurements = []
    sensor = Sensor(sensor_id, name, machine_id, measurements)
    return sensor

def get_sensor_objects(conn) -> list[Sensor]:
    try:
        sensors = []
        cursor = conn.execute("SELECT id, name, machine_id FROM sensors" ) 
        rows = cursor.fetchall()
        for row in rows:
            sensor = row_to_sensor(row)
            sensors.append(sensor)
        return sensors
    except Error as e:
        return sensors

def get_machines_with_sensors(conn) -> list[Machine]:
    machines = get_machine_objects(conn)
    sensors = get_sensor_objects(conn)
    for machine in machines:
        machine_id = machine.id
        for sensor in sensors:
            if sensor.machine_id == machine_id:
                machine.sensors.append(sensor)
    return machines

def insert_measurement(conn,
                       value: float,
                       unit: str,
                       sensor_id: int,
                       timestamp: str):
    cursor = conn.execute("SELECT id FROM sensors")
    rows = cursor.fetchall()
    sensor_ids = [row[0] for row in rows]
    if not sensor_id in sensor_ids:
        print("invalid sensor id")
        return
    try:
        sql_insert = "INSERT INTO measurements (value, unit, sensor_id, timestamp) VALUES (?,?,?,?)"
        conn.execute(sql_insert, (value, unit.strip(), sensor_id, timestamp))
        conn.commit()
    except Error as e:
        print(f"Error inserting sensors: {e}")  


def row_to_measurement(row) -> Measurement:
    value = row[1]
    unit = row[2]
    sensor_id = str(row[3])
    timestamp_str = row[4]  
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    measurement = Measurement(value, unit, sensor_id, timestamp)
    return measurement

def get_measurement_objects(conn) -> list[Measurement]:
    try:
        measurements = []
        cursor = conn.execute("SELECT id, value, unit, sensor_id, timestamp FROM measurements")
        rows = cursor.fetchall()
        for row in rows:
            measurement = row_to_measurement(row)
            measurements.append(measurement)
        return measurements
    except Error as e:
        print(f"{e}")
        return measurements

def get_complete_machines(conn) -> list[Machine]:
    machines = get_machines_with_sensors(conn)
    measurements = get_measurement_objects(conn)
    for measurement in measurements:
        sensor_id = measurement.sensor_id
        for machine in machines:
            for sensor in machine.sensors:
                if sensor.id == sensor_id:
                    sensor.measurements.append(measurement)
                    break
    return machines

def find_machine_by_id(
        machines: list[Machine],
        machine_id: str
) -> Machine | None:
    for machine in machines:
        if machine.id == machine_id:
            return machine
    return None

def find_sensor_by_id(
        machines: list[Machine],
        sensor_id: str
) -> Sensor | None:
    for machine in machines:
        for sensor in machine.sensors:
            if sensor.id == sensor_id:
                return sensor
    return None

def get_measurements_for_sensor(
        machines: list[Machine],
        sensor_id: str
) -> list[Measurement]:
    for machine in machines:
        for sensor in machine.sensors:
            if sensor.id == sensor_id:
                return sensor.measurements
    return []

def get_average_for_sensor(
        machines: list[Machine],
        sensor_id: str
) -> float | None:
    measurements = get_measurements_for_sensor(machines, sensor_id)
    if measurements:
        total = 0
        n = 0
        for measurement in measurements:
            total += measurement.value
            n += 1
        average = total / n
        return average
    return None

def get_highest_measurement_for_sensor(
        machines: list[Machine],
        sensor_id: str
) -> Measurement | None:
    measurements = get_measurements_for_sensor(machines, sensor_id)
    if measurements:
        highest = measurements[0]
        for measurement in measurements:
            if measurement.value > highest.value:
                highest = measurement
        return highest
    return None

def find_sensors_by_name(
        machines: list[Machine],
        sensor_name: str
) -> list[Sensor]:
    sensors = []
    if machines:
        for machine in machines:
            for sensor in machine.sensors:
                if sensor.name == sensor_name:
                    sensors.append(sensor)
    return sensors

def get_average_for_sensor_name(
        machines: list[Machine],
        sensor_name: str
) -> float | None:
    sensors = find_sensors_by_name(machines, sensor_name)
    if sensors:
        total = 0
        n = 0
        for sensor in sensors:
            if sensor.measurements:
                for measurement in sensor.measurements:
                    total += measurement.value
                    n += 1
        if n:
            return total / n
    return None





