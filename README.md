[![codecov](https://codecov.io/gh/carpetri/elevator/branch/main/graph/badge.svg)](https://codecov.io/gh/carpetri/elevator/)
# Elevator System

## Run
Simple test case included in the `input.json` file sample.
```
python elevatorSystemSimulator.py
```

To set a different configuration run the help cmd to see the instructions on how to set the parameters.
`python elevatorSystemSimulator.py -h`

```
usage: elevatorSystemSimulator.py [-h] [-ne NUM_ELEVATORS] [-nf NUM_FLOORS]
                                  [-c CAPACITY] [-v]
                                  [input_file] [output_file]

Elevator System Simulation.

positional arguments:
  input_file            The input file path with passenger requests.
  output_file           The output file path.

options:
  -h, --help            show this help message and exit
  -ne NUM_ELEVATORS, --num-elevators NUM_ELEVATORS
                        Number of elevators in the building.
  -nf NUM_FLOORS, --num-floors NUM_FLOORS
                        Number of floors in the building.
  -c CAPACITY, --capacity CAPACITY
                        Passenger capacity in each elevator.
  -v, --verbose         Enable debug mode.
  -a, --animate         Enable animation.
```

### Input
The input is a file with a `json` object per line representing each passenger in the queue. 

### Output
The output is `json` object that has detailed output of each time unit.

## Classes:
- An Elevator class to manage individual elevator states (current floor, direction, occupancy).
- ElevatorSystem class to manage the elevators and handle requests.
- Passenger class to manage the requests and total/waiting times and details.

## Scheduling Algorithm

Algorithm considering the minimun proximity of elevators to request floors and considering occupancy.

Other options to consider:
- Prioritize Requests by Wait Time
- Dynamic Re-evaluation
- Implement Load Balancing Among Elevators
- Consider Elevator Direction
- Optimize for Idle Time
- Advanced Algorithms: Nearest Car, Collective Control, or Destination Dispatch. See [link](https://peters-research.com/index.php/papers/elevator-dispatching/)


## Request Handling
Requests ase based on the time unit, ensuring no "looking ahead" in the request queue.

## Time Management
Included a time control mechanism to simulate the passing of time and the handling of requests in a time-ordered fashion.

## Logging and Statistics:
- Elevator Systems logs elevator positions at each time unit.
- Passenger class will save the data needed for the needed stats.

## Testing and Validation:
See the test cases file. Run with:
`pytest`

## Sample animation

### One elevator

![](https://github.com/carpetri/elevator/blob/main/sample_animations/elevator_animation.gif)

#### Results

```
  Min Wait Time  0.00
  Max Wait Time 33.00
 Mean Wait Time 14.75
 Min Total Time  9.00
 Max Total Time 34.00
Mean Total Time 23.75
```

### Two elevators

![](https://github.com/carpetri/elevator/blob/main/sample_animations/elevator_animation_ne2.gif)

### Results

```
  Min Wait Time  0.00
  Max Wait Time 10.00
 Mean Wait Time  3.25
 Min Total Time  2.00
 Max Total Time 19.00
Mean Total Time 12.25
```

### Three elevators

![](https://github.com/carpetri/elevator/blob/main/sample_animations/elevator_animation_ne3.gif)

### Results
```
  Min Wait Time  0.00
  Max Wait Time 10.00
 Mean Wait Time  3.25
 Min Total Time  2.00
 Max Total Time 19.00
Mean Total Time 12.25
```

### Long Sample

See file `generate_data.py`. It generates a sample input file. I created a sample file with 100 passengers that arrive within times `0-10` with random `source` and `destination`. 

The parameters of the simulation are the following:
- 3 Elevtors
- 20 Floors 
- 10 person capacity

To run: 

`./elevatorSystemSimulator.py -ne 3 -nf 20 -c 10 long_sample.json long_out.json -a`

![](https://github.com/carpetri/elevator/blob/main/sample_animations/long_animation.gif)

### Results 

```
  Min Wait Time   0.00
  Max Wait Time 115.00
 Mean Wait Time  38.31
 Min Total Time   4.00
 Max Total Time 122.00
Mean Total Time  45.14
```