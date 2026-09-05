import task15_modelARealDomain as myModel
from datetime import datetime

MA = myModel.Machine("MA", "MachineA")
MB = myModel.Machine("MB", "MachineB")

S1 = myModel.Sensor("S1", "engine_temperature")
S2 = myModel.Sensor("S2", "engine_pressure")
S3 = myModel.Sensor("S3", "engine_temperature")
S4 = myModel.Sensor("S4", "engine_pressure")

M11 = myModel.Measurement(80, "C", datetime.now())
M12 = myModel.Measurement(82, "C", datetime.now())
M21 = myModel.Measurement(90, "C", datetime.now())
M22 = myModel.Measurement(92, "C", datetime.now())

myModel.add_measurement(S1, M11)
myModel.add_measurement(S1, M12)
myModel.add_measurement(S3, M21)
myModel.add_measurement(S3, M22)

myModel.add_sensor(MA, S1)
myModel.add_sensor(MA, S2)
myModel.add_sensor(MB, S3)
myModel.add_sensor(MB, S4)

def find_sensors_by_name(machines: list[myModel.Machine],sensor_name: str) -> list[myModel.Sensor]:
    sensors = []
    for machine in machines:
        for sensor in machine.sensors:
            if sensor.name == sensor_name:
                sensors.append(sensor)

    return sensors

def average_across_machines(machines: list[myModel.Machine], sensor_name: str) -> float | None:
    sensors = find_sensors_by_name(machines, sensor_name)
    if not sensors:
        return None

    total = 0
    n = 0
    for sensor in sensors:
        for measurement in sensor.measurements:
            n += 1
            total += measurement.value

    if n == 0:
        return None

    average = total / n

    return average

if __name__ == "__main__":
    print(average_across_machines([MA, MB], "engine_temperature"))
