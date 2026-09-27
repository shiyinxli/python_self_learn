from task15_modelARealDomain import Machine, Measurement, Sensor
from rdflib import Graph, URIRef, Literal
from datetime import datetime
from rdflib import Namespace

def create_machine_triples(machine: Machine) -> list[tuple]:
    triples = []

    machine_uri = "http://example.com/machine/" + str(machine.id)

    i = 1

    for sensor in machine.sensors:
        sensor_uri = "http://example.com/sensor/" + str(sensor.id)

        triples.append(
            (machine_uri, "hasSensor", sensor_uri)
        )

        for measurement in sensor.measurements:
            measurement_uri = (
                "http://example.com/measurement/" + str(i)
            )

            triples.append(
                (sensor_uri, "hasMeasurement", measurement_uri)
            )
            triples.append(
                (measurement_uri, "hasValue", measurement.value)
            )
            triples.append(
                (measurement_uri, "hasUnit", measurement.unit)
            )
            triples.append(
                (measurement_uri, "hasTimestamp", measurement.timestamp)
            )

            i += 1

    return triples

# def create_rdf_graph(machine: Machine) -> Graph:
#     graph = Graph()

#     machine_uri = URIRef("http://example.com/machine/"+str(machine.id))
#     has_sensor = URIRef("http://example.com/hasSensor")
#     has_measurement = URIRef("http://example.com/hasMeasurement")
#     has_value = URIRef("http://example.com/hasValue")
#     has_unit = URIRef("http://example.com/hasUnit")
#     has_timestamp = URIRef("http://example.com/hasTimestamp")
#     i = 1
#     for sensor in machine.sensors:
#         sensor_uri = URIRef("http://example.com/sensor/"+str(sensor.id))
#         graph.add((machine_uri, has_sensor, sensor_uri))
#         for measurement in sensor.measurements:
#             measurement_uri = URIRef("http://example.com/measurement/"+str(i))
#             graph.add((sensor_uri, has_measurement, measurement_uri))
#             graph.add((measurement_uri, has_value, Literal(measurement.value)))
#             graph.add((measurement_uri, has_unit, Literal(measurement.unit)))
#             graph.add((measurement_uri, has_timestamp, Literal(measurement.timestamp)))
#             i += 1
#     return graph

def create_rdf_graph(machine: Machine) -> Graph:
    graph = Graph()
    ex = Namespace("http://example.com/")
    graph.bind("ex", ex)
    machine_uri = ex[f"machine/{machine.id}"]
    i = 1
    for sensor in machine.sensors:
        sensor_uri = ex[f"sensor/{sensor.id}"]
        graph.add((machine_uri, ex.hasSensor, sensor_uri))
        for measurement in sensor.measurements:
            measurement_uri = ex[f"measurement/{i}"]
            graph.add((sensor_uri, ex.hasMeasurement, measurement_uri))
            graph.add((measurement_uri, ex.hasValue, Literal(measurement.value)))
            graph.add((measurement_uri, ex.hasUnit, Literal(measurement.unit)))
            graph.add((measurement_uri, ex.hasTimestamp, Literal(measurement.timestamp)))
            i += 1
    return graph



if __name__ == "__main__":
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

    print("turtle format: ")
    print(graph.serialize(format="turtle"))

    print("xml format: ")
    print(graph.serialize(format="xml"))

    print("json format: ")
    print(graph.serialize(format="json-ld"))
