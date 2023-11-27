class Elevator:
    """Represents an elevator in the system."""
    def __init__(self, id, capacity):
        self.id = "E" + str(id)
        self.current_floor = 1
        self.direction = None
        self.capacity = capacity
        self.passengers = []

    def is_full(self):
        """Checks if the elevator is at full capacity."""
        return len(self.passengers) >= self.capacity

    def is_empty(self):
        """Checks if the elevator is at full capacity."""
        return len(self.passengers) == 0

    def load_passenger(self, passenger):
        """Loads a passenger into the elevator."""
        if not self.is_full():
            self.passengers.append(passenger)

    def unload_passenger(self, passenger):
        """Unloads a passenger from the elevator."""
        if passenger in self.passengers[:]:
            self.passengers.remove(passenger)