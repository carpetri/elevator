# Elevator System

## Approach to Development
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
See the test cases. 

