from .passenger import Passenger
from .elevator import Elevator
import logging
import pandas as pd

class ElevatorSystem:
    """Manages the elevators and passenger requests."""   
    logger = logging.getLogger(__name__)
    
    def __init__(self, num_elevators, num_floors, elevator_capacity):
        self.elevators = [Elevator(i+1,elevator_capacity) for i in range(num_elevators)]
        self.num_floors = num_floors
        self.requests = []
        self.processed_requests = []
        self.time = 0
        self.log = []

    def add_passenger_request(self, passenger):
        """Adds a new passenger request to the system."""
        if isinstance(passenger, Passenger):
            self.requests.append(passenger)
        else:
            raise TypeError("Needs to be a Passenger object.")

    def schedule_elevators(self):
        """Schedules elevators to fulfill requests."""
        for request in self.requests[:]:
            # Find the closest available elevator
            closest_elevator = min(
                self.elevators, 
                key=lambda e: abs(e.current_floor - request.source_floor) if not e.is_full() else float('inf')
            )
            if not closest_elevator.is_full():
                ElevatorSystem.logger.debug(f"Passenger {request.id} is assigned into elevator {closest_elevator.id}")
                closest_elevator.load_passenger(request)
                self.requests.remove(request)
            else:
                request.assignation_wait_time += 1
                ElevatorSystem.logger.debug(f"Passenger {request.id} is waiting. Elevator is full adding wait_time: {request.wait_time()}")

    def move_passengers(self):
        for elevator in self.elevators:
            if elevator.passengers[:]:
                for passenger in elevator.passengers[:]:
                    if passenger.target_floor == elevator.current_floor:
                        passenger.dropoff_time = self.time
                        if not passenger.pickup_time is None:  
                            self.processed_requests.append(passenger)
                            elevator.unload_passenger(passenger)
                            ElevatorSystem.logger.debug(f"Elevator {elevator.id}.\n\tUnloading passenger: {passenger.id}")
                            ElevatorSystem.logger.debug(f"\tRemaining passengers: {[p.id for p in self.requests]}")
                    # Mark the pickup_time
                    if passenger.source_floor == elevator.current_floor  :
                        ElevatorSystem.logger.debug(f"Elevator {elevator.id} is at floor {elevator.current_floor} passenger {passenger.id} is picked up.")
                        passenger.pickup_time = self.time
    
    def move_elevators(self):
        """Moves elevators according to scheduling."""
        for elevator in self.elevators:
            if elevator.passengers:
                # Move towards the nearest passenger's destination on board
                on_board_passengers = [p for p in elevator.passengers if p.pickup_time is not None]
                if on_board_passengers:
                    nearest_passenger = min(on_board_passengers, key=lambda p: abs(elevator.current_floor - p.target_floor))
                    ElevatorSystem.logger.debug(f"Elevator {elevator.id} is t floor {elevator.current_floor} going to drop {nearest_passenger.id} at {nearest_passenger.target_floor}")
                    if elevator.current_floor < nearest_passenger.target_floor:
                        elevator.current_floor += 1
                    elif elevator.current_floor > nearest_passenger.target_floor:
                        elevator.current_floor -= 1
                else:
                    # Move towards the nearest source
                    waiting_passengers = [p for p in elevator.passengers if p.pickup_time is None]
                    nearest_passenger = min(waiting_passengers, key=lambda p: abs(elevator.current_floor - p.source_floor))
                    ElevatorSystem.logger.debug(f"Elevator {elevator.id} is at floor {elevator.current_floor} going to pick {nearest_passenger.id} at {nearest_passenger.source_floor}")
                    if elevator.current_floor < nearest_passenger.source_floor:
                        elevator.current_floor += 1
                    elif elevator.current_floor > nearest_passenger.source_floor:
                        elevator.current_floor -= 1

    def all_requests_processed(self):
        """Checks if all requests have been processed."""
        return len(self.requests) == 0 and all(len(e.passengers) == 0 for e in self.elevators)

    def log_positions(self):
        """Log the positions of the elevators and passengers"""
        
        # Passengers waiting
        passenger_positions = {passenger.id: passenger.current_floor(self.time) for passenger in self.requests}
        
        # Passengers traveling
        for e in self.elevators:
            passenger_positions.update({p.id: p.current_floor(self.time) for p in e.passengers})
        
        snapshot = {
            'time': self.time,
            'positions': {e.id: e.current_floor for e in self.elevators},
            'passengers_assigned': {elevator.id : [ passenger.id for passenger in elevator.passengers ] for elevator in self.elevators},
            'passengers_positions': passenger_positions,
        }

        ElevatorSystem.logger.debug(f"Passenger positions: { " ".join( [ f"- {p}: {pos}" for p,pos in passenger_positions.items()]) }")
        self.log.append(snapshot)
    
    def move_time(self):
        """Funny named function that advances the system by one time unit."""
        ElevatorSystem.logger.debug(f'\nTime is {self.time}')
        self.schedule_elevators()
        self.log_positions()
        self.move_passengers()
        self.move_elevators()
        self.time += 1

    def time_summary(self):
        """Summary of the requests"""
        passenger_stats = []
        for passenger in self.processed_requests:
            passenger_stats.append({
                'Passenger ID': passenger.id,
                'Wait Time': passenger.wait_time(),
                'Total Time': passenger.total_time()
            })

        passenger_stats_df = pd.DataFrame(passenger_stats)
        ElevatorSystem.logger.debug(passenger_stats_df)

        stats_summary = passenger_stats_df.agg({
            'Wait Time': ['min', 'max', 'mean'],
            'Total Time': ['min', 'max', 'mean']
        })
        
        stats_summary.reset_index(inplace=True)
        long_format_data = stats_summary.melt(id_vars='index', var_name='var', value_name='Value')
        long_format_data['Variable'] = long_format_data['index'].str.capitalize() + ' ' + long_format_data['var']

        return(long_format_data[["Variable", "Value"]].to_string(index=False, header=False))
        

