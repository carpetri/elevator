#!/usr/bin/env python3

import pandas as pd
import json
from collections import deque 
import os
import logging
import sys
from models.passenger import Passenger
from models.elevatorSystem import ElevatorSystem
import argparse

########################################################
# Parse parameters for simulation
########################################################

# Create the parser
parser = argparse.ArgumentParser(description="Elevator System Simulation.")

# input and output files
parser.add_argument('input_file', type=str, nargs='?', default="input.json", help='The input file path with passenger requests.')
parser.add_argument('output_file', type=str, nargs='?', default="elevator_time.log", help='The output file path.')

# Assumed a fixed numer of elevators and all the elevators are equal.
# Elevators in the future could have different capacities and restrictions on floors.
# Toy parameters
parser.add_argument('-ne', '--num-elevators', type=int, required=False, default=1, help='Number of elevators in the building.')
parser.add_argument('-nf', '--num-floors', type=int, required=False, default=10, help='Number of floors in the building.')
parser.add_argument('-c', '--capacity', type=int, required=False, default = 2, help='Passenger capacity in each elevator.')

#Verbose
parser.add_argument('-v', '--verbose', action='store_true', help='Enable debug mode.')

# Parse arguments
args = parser.parse_args()

# Access the input/output
input_file = args.input_file
output_file = args.output_file

#Simulation parameters
num_elevators= args.num_elevators
num_floors = args.num_floors
elevator_capacity = args.capacity

#debug mode
verbose_mode = args.verbose

########################################################
# Setup Logging 
########################################################

log_level = logging.DEBUG if verbose_mode else logging.INFO
logger = logging.getLogger(__name__)
fmt = '%(message)s'
logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)


########################################################
# Simulation function
########################################################
def run_simulation(num_elevators, num_floors, elevator_capacity, input_requests, file_log = output_file):
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
            elevator_system.add_passenger_request(passenger)
        elevator_system.move_time()

    # Adding Extra time to show the empty elevators at the end of the log
    elevator_system.move_time()

    # Write log to file 
    with open(file_log, "w") as f:
        json.dump(elevator_system.log, f, indent=4)
    return elevator_system


########################################################
# Simulation Run
########################################################

if __name__ == "__main__":
    # Took the approach of reading json per line because would more closely simulate a json request. 
    # In the future this could be a Stream of data
    input_requests = []
    with open(input_file, 'r') as file:
        for line in file:
            input_requests.append(json.loads(line))

    # Run simulation
    elevator_system = run_simulation(num_elevators, num_floors, elevator_capacity, input_requests)

    # Time summary
    print(elevator_system.time_summary())
