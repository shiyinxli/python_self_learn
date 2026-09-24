from task27_repository import MachineRepository, SensorRepository, MeasurementRepository
class MachineService:
    def __init__(self, machine_repo, sensor_repo, measure_repo):
        self.machine_repo = machine_repo
        self.sensor_repo = sensor_repo
        self.measure_repo = measure_repo

    def get_average_temperature(self, machine_id: str) -> float | None:
        sensors = self.sensor_repo.get_by_machine_id(machine_id)
        total = 0
        n = 0
        for sensor in sensors:
            if sensor.name == "Temperature":
                sensor_id = sensor.id
                measurements = self.measure_repo.get_by_sensor_id(sensor_id)
                for measurement in measurements:
                    total += measurement.value
                    n += 1
        if n != 0:
            return total / n
        return None

        
