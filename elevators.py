import pandas as pd
import json
from collections import deque 
import os

DEBUG = os.getenv("DEBUG_ELEVATORS", False)
def my_print(s):
    if DEBUG:
        print(s)

class Passenger:
    """Represents a passenger in the elevator system."""
    def __init__(self, id, source_floor, target_floor, request_time):
        self.id = id
        self.source_floor = source_floor
        self.target_floor = target_floor
        self.request_time = request_time
        #self.direction = "up" if source_floor < target_floor else "down"
        self.pickup_time = None
        self.dropoff_time = None
        self.assignation_wait_time = 0

    def wait_time(self):
        """Calculates the wait time for the passenger."""
        if self.pickup_time:
            return self.assignation_wait_time + self.pickup_time - self.request_time  if not self.pickup_time is None else None
        
        #Just for logging needs
        return self.assignation_wait_time 
  
    def total_time(self):
        """Calculates the total time for the passenger's journey."""
        return self.dropoff_time - self.request_time   if not self.pickup_time is None else None

class Elevator:
    """Represents an elevator in the system."""
    def __init__(self, id, capacity):
        self.id = "E" + str(id)
        self.current_floor = 1
        self.capacity = capacity
        self.passengers = []

    def is_full(self):
        """Checks if the elevator is at full capacity."""
        return len(self.passengers) >= self.capacity

    def load_passenger(self, passenger):
        """Loads a passenger into the elevator."""
        if not self.is_full():
            self.passengers.append(passenger)

    def unload_passenger(self, passenger):
        """Unloads a passenger from the elevator."""
        if passenger in self.passengers[:]:
            self.passengers.remove(passenger)

class ElevatorSystem:
    """Manages the elevators and passenger requests."""
    def __init__(self, num_elevators, num_floors, elevator_capacity):
        self.elevators = [Elevator(i+1,elevator_capacity) for i in range(num_elevators)]
        self.num_floors = num_floors
        self.requests = []
        self.processed_requests = []
        self.time = 0
        self.log = []

    def add_person_request(self, passenger):
        """Adds a new passenger request to the system."""
        self.requests.append(passenger)

    def schedule_elevators(self):
        """Schedules elevators to fulfill requests."""
        for request in self.requests[:]:
            # Find the closest available elevator
            #my_print( f"time is {self.time} and person is {request.id}")
            closest_elevator = min(
                self.elevators, 
                key=lambda e: abs(e.current_floor - request.source_floor) if not e.is_full() else float('inf')
            )
            if not closest_elevator.is_full():
                my_print(f"Time {self.time}. passenger {request.id} is assigned into elevator {closest_elevator.id}")
                closest_elevator.load_passenger(request)
                self.requests.remove(request)
            else:
                request.assignation_wait_time += 1
                my_print(f"Time is {self.time} Person {request.id} is waiting. elevator is full adding wait_time: {request.wait_time()}")
                #my_print(f"current wait_time {request.wait_time()}")
                #my_print(f"floor is {closest_elevator.current_floor}")

    def move_passengers(self):
        for elevator in self.elevators:
            if elevator.passengers[:]:
                for passenger in elevator.passengers[:]:
                    if passenger.target_floor == elevator.current_floor:
                        passenger.dropoff_time = self.time
                        if not passenger.pickup_time is None:  
                            self.processed_requests.append(passenger)
                            elevator.unload_passenger(passenger)
                            my_print(f"Unloading: {passenger.id}")
                            my_print(f"Remaining: {[p.id for p in self.requests]}")
                    # Mark the pickup_time
                    if passenger.source_floor == elevator.current_floor  :
                        my_print(f"floor is {elevator.current_floor} passenger {passenger.id} is picked at time {self.time}")
                        passenger.pickup_time = self.time
    
    def move_elevators(self):
        """Moves elevators according to scheduling."""
        for elevator in self.elevators:
            if elevator.passengers:
                # Move towards the nearest passenger's destination on board
                on_board_passengers = [p for p in elevator.passengers if p.pickup_time is not None]
                if on_board_passengers:
                    nearest_passenger = min(on_board_passengers, key=lambda p: abs(elevator.current_floor - p.target_floor))
                    my_print(f"At floor {elevator.current_floor} going to drop {nearest_passenger.id} at {nearest_passenger.target_floor}")
                    if elevator.current_floor < nearest_passenger.target_floor:
                        elevator.current_floor += 1
                    elif elevator.current_floor > nearest_passenger.target_floor:
                        elevator.current_floor -= 1
                else:
                    # Move towards the nearest source
                    waiting_passengers = [p for p in elevator.passengers if p.pickup_time is None]
                    nearest_passenger = min(waiting_passengers, key=lambda p: abs(elevator.current_floor - p.source_floor))
                    my_print(f"At floor {elevator.current_floor} going to pick {nearest_passenger.id} at {nearest_passenger.source_floor}")
                    if elevator.current_floor < nearest_passenger.source_floor:
                        elevator.current_floor += 1
                    elif elevator.current_floor > nearest_passenger.source_floor:
                        elevator.current_floor -= 1

    def all_requests_processed(self):
        """Checks if all requests have been processed."""
        return len(self.requests) == 0 and all(len(e.passengers) == 0 for e in self.elevators)

    def log_positions(self):
        # Log the positions of the elevators
        self.log.append({
            'time': self.time,
            'positions': {e.id: e.current_floor for e in self.elevators},
            'passengers_assigned': {elevator.id : [ passenger.id for passenger in elevator.passengers ] for elevator in self.elevators}
        })
    
    def move_time(self):
        """Funny named function that advances the system by one time unit."""
        my_print(f'\nTime is {self.time}')
        self.schedule_elevators()
        self.log_positions()
        self.move_passengers()
        self.move_elevators()
        self.time += 1

########################################################
# Simulation
########################################################
def run_simulation(num_elevators, num_floors, elevator_capacity, input_requests, file_log = "elevator_time.log"):
    elevator_system = ElevatorSystem(num_elevators, num_floors, elevator_capacity)
    # Will stop until all passangers have been proccessed and reached destination.
    input_requests = deque(input_requests)
    total_requests = len(input_requests)
    while input_requests or not len(elevator_system.processed_requests) == total_requests:
        # Add request up to the current system time.
        while input_requests and input_requests[0]["time"]==elevator_system.time:
            request = input_requests.popleft()
            # Creating a Passenger object per request to store metrics
            passenger = Passenger(request['id'], request['source'], request['dest'], request['time'])
            elevator_system.add_person_request(passenger)
        elevator_system.move_time()

    #Adding Extra time to show the empty elevators at the end
    elevator_system.move_time()


    #wirte log to file 
    with open(file_log, "w") as f:
        json.dump(elevator_system.log, f, indent=4)  # 4 spaces
    return elevator_system




if __name__ == "__main__":
    ########################################################
    # Read sample input and parameters
    ########################################################
    # Took the approach of reading json per line because would more closely simulate a json request.
    # In the future this could be a Stream of data

    # Request as queue.
    input_requests = []
    with open("input.json", 'r') as file:
        for line in file:
            input_requests.append(json.loads(line))

    # Toy parameters
    # Assumed a fixed numer of elevators and all the elevators are equal.
    # Elevators in the future could have different capacities and restrictions on floors.
    num_elevators = 1
    num_floors = 10
    elevator_capacity = 2

    #run simulation
    elevator_system = run_simulation(num_elevators, num_floors, elevator_capacity, input_requests)

    ########################################################
    # Stats
    ########################################################
    passenger_stats = []
    # Calculate statistics
    for passenger in elevator_system.processed_requests:
        passenger_stats.append({
            'Passenger ID': passenger.id,
            'Wait Time': passenger.wait_time(),
            'Total Time': passenger.total_time()
        })

    passenger_stats_df = pd.DataFrame(passenger_stats)
    my_print(passenger_stats_df)

    stats_summary = passenger_stats_df.agg({
    'Wait Time': ['min', 'max', 'mean'],
    'Total Time': ['min', 'max', 'mean']
    })
    
    stats_summary.reset_index(inplace=True)
    long_format_data = stats_summary.melt(id_vars='index', var_name='var', value_name='Value')
    long_format_data['Variable'] = long_format_data['index'].str.capitalize() + ' ' + long_format_data['var']


    print(long_format_data[["Variable", "Value"]].to_string(index=False, header=False))


