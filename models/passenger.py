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
        self.assignation_wait_time = 0
        self.assigned_elevator = None

    def wait_time(self):
        """Calculates the wait time for the passenger."""
        if not self.pickup_time is None:
            return self.pickup_time - self.request_time  if not self.pickup_time is None else None
        
        #Just for logging needs while pickup time is not ready
        return self.assignation_wait_time 
  
    def total_time(self):
        """Calculates the total time for the passenger's journey."""
        return self.dropoff_time - self.request_time   if not self.pickup_time is None else None

    def current_floor(self, current_time):
        """Logs the current floor of a passenger"""

        # Passenger is waiting to get in
        if self.pickup_time is None:
            return self.source_floor
        
        # Passenger got to their destination
        if self.dropoff_time is not None:
            return self.target_floor

        sign = 1 if self.source_floor < self.target_floor else -1
        return self.source_floor + sign*abs(current_time - self.pickup_time) 

    def current_status(self):
        """Logs the Status passenger. W: Waiting, T: Traveling, D: Done"""

        # Passenger is waiting to get in
        if self.pickup_time is None:
            return "W"
        
        # Passenger got to their destination
        if self.dropoff_time is None:
            return "T"

        return "D"