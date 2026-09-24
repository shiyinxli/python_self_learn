from task15_modelARealDomain import Machine, Sensor, Measurement
from task18_databaseModeling import (get_complete_machines, get_machine_objects, find_machine_by_id,
                                     insert_machine, get_sensor_objects, insert_measurement, insert_sensor,
                                     get_measurement_objects, row_to_measurement, get_measurements_for_sensor)

class MachineRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_all(self) -> list[Machine]:
        machines = get_complete_machines(self.conn)
        return machines

    def get_by_id(self, machine_id: str) -> Machine | None:
        sql = "SELECT id, name FROM machines WHERE id = ?"
        cursor = self.conn.execute(sql, (machine_id.strip(),))
        row = cursor.fetchone()

        if row is None: 
            return None
        return Machine(id=row[0], name=row[1])
        
    def add(self, name: str) -> None:
        insert_machine(self.conn, name)

class SensorRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_all(self) -> list[Sensor]:
        sensors = get_sensor_objects(self.conn)
        return sensors

    def get_by_id(self, sensor_id: str) -> Sensor | None:
        sql = "SELECT id, name, machine_id FROM sensors WHERE id = ?"
        cursor = self.conn.execute(sql, (sensor_id.strip(),))
        row = cursor.fetchone()

        if row is None: 
            return None
        return Sensor(id=row[0], name=row[1], machine_id=row[2])
        
    def add(self, name: str, machine_id: int) -> None:
        insert_sensor(self.conn, name, machine_id)

    def get_by_machine_id(self, machine_id: str) -> list[Sensor]:
        sensors = []
        machines = get_complete_machines(self.conn)
        for machine in machines:
            if machine.id == machine_id:
                return machine.sensors
        return sensors

class MeasurementRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, value: float, unit: str, sensor_id: int, timestamp: str) -> None:
        insert_measurement(self.conn, value, unit, sensor_id, timestamp)

    def get_all(self) -> list[Measurement]:
        measurements = get_measurement_objects(self.conn)
        return measurements
    
    def get_by_id(self, measurement_id: str) -> Measurement | None:
        sql = "SELECT id, value, unit, sensor_id, timestamp FROM measurements WHERE id = ?"
        cursor = self.conn.execute(sql, (measurement_id.strip(), ))
        row = cursor.fetchone()
        if row:
            return row_to_measurement(row)
        return None

    def get_by_sensor_id(self, sensor_id: str) -> list[Measurement]:
        measurements = []
        sql = "SELECT id, value, unit, sensor_id, timestamp FROM measurements WHERE sensor_id = ?"
        cursor = self.conn.execute(sql, (sensor_id.strip(), ))
        rows = cursor.fetchall()
        for row in rows:
            measurement = row_to_measurement(row)
            measurements.append(measurement)
        return measurements
        





