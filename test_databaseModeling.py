from task18_databaseModeling import create_table, create_connection, get_machines, insert_machine, row_to_machine, get_machine_objects
from task15_modelARealDomain import Machine

def test_create_connection():
    conn = create_connection()
    assert conn is not None

def test_get_machines():
    conn = create_connection()
    create_table(conn)
    insert_machine(conn, "MachineA")
    rows = get_machines(conn)
    assert rows[0][1] == "MachineA"
    assert len(rows) == 1

def test_empty_database():
    conn = create_connection()
    create_table(conn)
    rows = get_machines(conn)
    assert rows == []

def test_multiple_machines():
    conn = create_connection()
    create_table(conn)
    insert_machine(conn, "MachineA")
    insert_machine(conn, "MachineB")
    rows = get_machines(conn)
    assert len(rows) == 2
    assert rows[0][1] == "MachineA"
    assert rows[1][1] == "MachineB"


def test_raw_conversion():
    row = (5, "MachineX")
    machine = row_to_machine(row)
    assert machine.id == "5"
    assert machine.name == "MachineX"
    assert machine.sensors == []

def test_multiple_database_record():
    conn = create_connection()
    create_table(conn)
    insert_machine(conn, "MachineA")
    insert_machine(conn, "MachineB")
    machines = get_machine_objects(conn)
    assert len(machines) == 2
    assert isinstance(machines[0], Machine)
    assert isinstance(machines[1], Machine)   

def test_empty_database_object():
    conn = create_connection()
    create_table(conn)
    machines = get_machine_objects(conn)
    assert machines == []
