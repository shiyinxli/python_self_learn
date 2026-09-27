from task15_modelARealDomain import Machine, Measurement, Sensor
from task27_repository import MachineRepository, SensorRepository, MeasurementRepository
import pytest
from datetime import datetime
from task18_databaseModeling import (create_connection, create_table)
from task28_service import MachineService
from task29_rdf import create_machine_triples, create_rdf_graph
from rdflib import Graph, URIRef, Literal


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

def test_create_machine_triples():
    measurement = Measurement(
        33.4,
        "C",
        "1",
        datetime.strptime(
            "2026-09-10 10:00:00",
            "%Y-%m-%d %H:%M:%S"
        )
    )

    sensor = Sensor(
        "1",
        "Temperature",
        "1",
        [measurement]
    )

    machine = Machine(
        "1",
        "MachineA",
        [sensor]
    )



    triples = create_machine_triples(machine)

    assert isinstance(triples, list)
    for t in triples:
        assert len(t) == 3


def test_multiple_sensors():
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

    triples = create_machine_triples(machine)
    print(triples)
    assert isinstance(triples, list)
    for t in triples:
        assert len(t) == 3

    

def test_create_rdf_graph():
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

    assert len(graph) == 18
    assert (
    URIRef("http://example.com/measurement/1"),
    URIRef("http://example.com/hasValue"),
    Literal(33.4)
) in graph

def test_serialization_rdf_graph():
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

    turtle_data = graph.serialize(format="turtle")
    assert isinstance(turtle_data, str)
    assert "hasSensor" in turtle_data
    assert "hasMeasurement" in turtle_data
    # assert "33.4" in turtle_data


