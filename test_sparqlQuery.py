from task15_modelARealDomain import Measurement, Machine, Sensor
from datetime import datetime
from task29_rdf import create_rdf_graph
from task36_sparqlQuery import get_sensors, get_sensor_measurements

def test_sparql_get_sensors():
    measurement1 = Measurement(
        33.4,
        "C",
        "1",
        datetime.strptime(
            "2026-09-10 10:00:00",
            "%Y-%m-%d %H:%M:%S"
        )
    )

    measurement2 = Measurement(
    34.1,
    "C",
    "1",
    datetime.strptime(
        "2026-09-10 10:00:00",
        "%Y-%m-%d %H:%M:%S"
    )
)
    measurement3 = Measurement(
        1.2,
        "bar",
        "2",
        datetime.strptime(
            "2026-09-10 10:00:00",
            "%Y-%m-%d %H:%M:%S"
        )
    )

    measurement4 = Measurement(
        1.3,
        "bar",
        "2",
        datetime.strptime(
            "2026-09-10 10:00:00",
            "%Y-%m-%d %H:%M:%S"
        )
    )

    sensor1 = Sensor(
        "1",
        "Temperature",
        "1",
        [measurement1, measurement2]
    )

    sensor2 = Sensor(
        "2",
        "Pressure",
        "1",
        [measurement3, measurement4]
    )

    machine = Machine(
        "1",
        "MachineA",
        [sensor1, sensor2]
    )

    graph = create_rdf_graph(machine)
    results = get_sensors(graph)
    for row in results:
        print(row)
    assert len(results) == 2

def test_get_sensor_measurement():
    measurement1 = Measurement(
        33.4,
        "C",
        "1",
        datetime.strptime(
            "2026-09-10 10:00:00",
            "%Y-%m-%d %H:%M:%S"
        )
    )

    measurement2 = Measurement(
    34.1,
    "C",
    "1",
    datetime.strptime(
        "2026-09-10 10:00:00",
        "%Y-%m-%d %H:%M:%S"
    )
)
    measurement3 = Measurement(
        1.2,
        "bar",
        "2",
        datetime.strptime(
            "2026-09-10 10:00:00",
            "%Y-%m-%d %H:%M:%S"
        )
    )

    measurement4 = Measurement(
        1.3,
        "bar",
        "2",
        datetime.strptime(
            "2026-09-10 10:00:00",
            "%Y-%m-%d %H:%M:%S"
        )
    )

    sensor1 = Sensor(
        "1",
        "Temperature",
        "1",
        [measurement1, measurement2]
    )

    sensor2 = Sensor(
        "2",
        "Pressure",
        "1",
        [measurement3, measurement4]
    )

    machine = Machine(
        "1",
        "MachineA",
        [sensor1, sensor2]
    )

    graph = create_rdf_graph(machine)
    results = get_sensor_measurements(graph)
    assert len(results) == 4
    


