import sqlite3
from sqlite3 import Error
from task15_modelARealDomain import Machine, Sensor, Measurement

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
    cursor = conn.execute("SELECT id, name, machine_id FROM sensors")
    sensors = get_sensor_objects(conn)
    for machine in machines:
        machine_id = machine.id
        for sensor in sensors:
            if sensor.machine_id == machine_id:
                machine.sensors.append(sensor)
    return machines





