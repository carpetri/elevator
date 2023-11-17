import pandas as pd
import json
from collections import deque 

class Passenger:
    """Represents a passenger in the elevator system."""
    def __init__(self, id, source_floor, target_floor, request_time):
        self.id = id
        self.source_floor = source_floor
        self.target_floor = target_floor
        self.request_time = request_time
        self.direction = "up" if source_floor < target_floor else "down"
        self.pickup_time = None
        self.dropoff_time = None

    def wait_time(self):
        """Calculates the wait time for the passenger."""
        return self.pickup_time - self.request_time  if not self.pickup_time is None else None

    def total_time(self):
        """Calculates the total time for the passenger's journey."""
        return self.dropoff_time - self.request_time  if not self.pickup_time is None else None

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
        if passenger in self.passengers:
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
            #print( f"time is {self.time} and request is {request.id}")
            closest_elevator = min(
                self.elevators, 
                key=lambda e: abs(e.current_floor - request.source_floor) if not e.is_full() else float('inf')
            )
            if not closest_elevator.is_full():
                closest_elevator.load_passenger(request)
                self.requests.remove(request)

    def move_passengers(self):
        for elevator in self.elevators:
            if elevator.passengers:
                for passenger in elevator.passengers[:]:
                    if passenger.target_floor == elevator.current_floor:
                        passenger.dropoff_time = self.time
                        self.processed_requests.append(passenger)
                        elevator.unload_passenger(passenger)
                    # Mark the pickup_time
                    if passenger.source_floor == elevator.current_floor:
                        passenger.pickup_time = self.time
    
    def move_elevators(self):
        """Moves elevators according to scheduling."""
        for elevator in self.elevators:
            if elevator.passengers:
                # Move towards the nearest passenger's destination
                nearest_passenger = min(elevator.passengers, key=lambda p: abs(elevator.current_floor - p.target_floor))
                if elevator.current_floor < nearest_passenger.target_floor:
                    elevator.current_floor += 1
                elif elevator.current_floor > nearest_passenger.target_floor:
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
        self.schedule_elevators()
        self.log_positions()
        self.move_passengers()
        self.move_elevators()
        self.time += 1

########################################################
# Read sample input and parameters
########################################################
# Took the approach of reading json per line because would more closely simulate a json request.
# In the future this could be a Stream of data

# Request as queue.
input_requests = deque([])
with open("input.json", 'r') as file:
    for line in file:
        input_requests.append(json.loads(line))

# Toy parameters
# Assumed a fixed numer of elevators and all the elevators are equal.
# Elevators in the future could have different capacities and restrictions on floors.
num_elevators = 2
num_floors = 100
elevator_capacity = 10


########################################################
# Initialization
########################################################
elevator_system = ElevatorSystem(num_elevators, num_floors, elevator_capacity)


########################################################
# Simulation
########################################################

# Will stop until all passangers have been proccessed and reached destination.
while input_requests or not elevator_system.all_requests_processed():
    # Add request up to the current system time.
    while input_requests and input_requests[0]["time"]==elevator_system.time:
        request = input_requests.popleft()
        # Creating a Passenger object per request to store metrics
        passenger = Passenger(request['id'], request['source'], request['dest'], request['time'])
        elevator_system.add_person_request(passenger)
    elevator_system.move_time()

with open("elevator_time.log", "w") as f:
    json.dump(elevator_system.log, f, indent=4)  # 4 spaces

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
print(passenger_stats_df)

#
stats_summary = {
    'Min Wait Time': passenger_stats_df['Wait Time'].min(),
    'Max Wait Time': passenger_stats_df['Wait Time'].max(),
    'Mean Wait Time': passenger_stats_df['Wait Time'].mean(),
    'Min Total Time': passenger_stats_df['Total Time'].min(),
    'Max Total Time': passenger_stats_df['Total Time'].max(),
    'Mean Total Time': passenger_stats_df['Total Time'].mean()
}
print(stats_summary)
