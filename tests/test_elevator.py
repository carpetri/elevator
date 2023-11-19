import pytest
from elevators import Passenger, Elevator, ElevatorSystem, run_simulation

def test_single_passenger():
    input_data = {
        'num_elevators': 1,
        'num_floors': 5,
        'elevator_capacity': 4,
        'input_requests': [{'id': 1, 'source': 1, 'dest': 3, 'time': 0}]
    }
    elevator_system = run_simulation(**input_data)
    assert len(elevator_system.processed_requests) == 1
    assert elevator_system.all_requests_processed()
    assert elevator_system.processed_requests[0].total_time() == 2

def test_capacity_reached():
    input_data = {
        "num_elevators": 1,
        "num_floors": 10,
        "elevator_capacity": 2,
        "input_requests": [
            {"id": 1, "source": 2, "dest": 5, "time": 0},
            {"id": 2, "source": 3, "dest": 6, "time": 0},
            {"id": 3, "source": 1, "dest": 7, "time": 1}
        ]
    }
    elevator_system = run_simulation(**input_data)
    assert len(elevator_system.processed_requests) == 3
    assert [p.total_time() for p in  elevator_system.processed_requests] == [4, 5, 15]

def test_no_passengers():
    input_data= {
            "num_elevators": 2,
            "num_floors": 20,
            "elevator_capacity": 5,
            "input_requests": []
        }
    elevator_system = run_simulation(**input_data)
    assert len(elevator_system.processed_requests) == 0

def test_multiple_passengers_to_same_floor():
    input_data = {
        "num_elevators": 1,
        "num_floors": 15,
        "elevator_capacity": 10,
        "input_requests": [
            {"id": 1, "source": 3, "dest": 10, "time": 0},
            {"id": 2, "source": 4, "dest": 10, "time": 2},
            {"id": 3, "source": 5, "dest": 10, "time": 4}
        ]
    }
    elevator_system = run_simulation(**input_data)
    assert [p.total_time() for p in  elevator_system.processed_requests] == [9, 7, 5]

def test_passengers_after_system_starts():
    input_data= {
        "num_elevators": 1,
        "num_floors": 10,
        "elevator_capacity": 3,
        "input_requests": [
            {"id": 1, "source": 2, "dest": 8, "time": 1},
            {"id": 2, "source": 1, "dest": 9, "time": 5},
            {"id": 3, "source": 4, "dest": 7, "time": 10}
        ]
    }
    elevator_system = run_simulation(**input_data)
    assert len(elevator_system.processed_requests) == 3



        