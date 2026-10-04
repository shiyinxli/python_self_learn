from task15_modelARealDomain import Machine, Measurement, Sensor
from rdflib import Graph, URIRef, Literal
from datetime import datetime
from rdflib import Namespace

def get_sensors(graph: Graph):
    query = """
    PREFIX ex: <http://example.com/>
    SELECT ?sensor
    WHERE {
        ?machine ex:hasSensor ?sensor .
    }
    """
    results = graph.query(query)
    return results

# Task 37 — SPARQL joins: Sensor → Measurement
def get_sensor_measurements(graph: Graph):
    query = """
    PREFIX ex: <http://example.com/>
    SELECT ?sensor ?measurement
    WHERE{
        ?sensor ex:hasMeasurement ?measurement .
    }
    """
    results = graph.query(query)
    return results

