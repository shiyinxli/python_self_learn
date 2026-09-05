from task15_modelARealDomain import Sensor, Machine, Measurement
def average_measurement(sensor: Sensor) -> float | None:
    if len(sensor.measurements) == 0:
        return None
    values = []
    for measurement in sensor.measurements:
        values.append(measurement.value)
    average_measurement = sum(values) / len(values)
    return average_measurement

def highest_measurement(sensor: Sensor) -> Measurement | None:
    if len(sensor.measurements) == 0:
         return None
    current_highest = sensor.measurements[0]
    for m in sensor.measurements:
        if m.value > current_highest.value:
            current_highest = m
    return current_highest

