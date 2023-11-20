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
        if not self.pickup_time is None:
            return self.pickup_time - self.request_time  if not self.pickup_time is None else None
        
        #Just for logging needs while pickup time is not ready
        return self.assignation_wait_time 
  
    def total_time(self):
        """Calculates the total time for the passenger's journey."""
        return self.dropoff_time - self.request_time   if not self.pickup_time is None else None