import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import json
import pandas as pd
import random
from elevatorSystemSimulator import run_simulation

num_elevators, num_floors, elevator_capacity = 2, 20, 2

def parse_log_file(log_file = "plot.log"):
    with open(log_file, 'r') as file:
        dat = json.load(file)

    passenger_positions = []
    elevator_positions = []
    for t in dat:
        current_time = t.get("time")
        for passenger, position in t.get("passengers_positions").items():
            passenger_positions.append({
                "time": current_time, 
                "passenger": passenger, 
                "location": position["floor"],
                "status": position["status"],
                "elevator": position["elevator"]
                })
            cur_time = t.get("time")
        for elevator, position in t.get("positions").items():
            elevator_positions.append({"time": current_time, "elevator": elevator, "location": position})

    pp_df = pd.DataFrame(passenger_positions)
    ep_df = pd.DataFrame(elevator_positions)
    return pp_df, ep_df

passenger_positions_df, elevator_positions_df = parse_log_file()

max_time = elevator_positions_df.time[-1:].values[0]

# Elevator and building setup
floors = num_floors
min_floor = 1
elevators = elevator_positions_df.elevator.unique()
num_elevators = len(elevators)
elevator_positions = [min_floor]*num_elevators
ele_marker_size = 5
points_size = 2

# def create_plot(floors, min_floor = 1, num_elevators = 2, ele_marker_size = 5, points_size = 2):
#     elevator_positions = [min_floor]*num_elevators
#     return plt
# Create figure and axes
plt.rcParams['figure.figsize'] = [(num_elevators+3)*1.5,(floors//5)*1.5]
fig, ax = plt.subplots()

# Use square markers for elevators and increase size
elevator_lines = [ax.plot(1 + i, elevator_positions[i], 's', markersize=ele_marker_size, color = "black")[0] for i in range(num_elevators)]

# Initialize time variable
current_time = 0

# Auto update function
def auto_update(frame):
    global current_time
    if current_time>=max_time:
        return
    current_time += 1
    slider.set_val(current_time)
    update_elevator_positions()

# Slider update function
def slider_update(val):
    global current_time
    current_time = int(val)
    update_elevator_positions()

def setup_plot(ax):
    global current_time
    ax.set_xlim(0.5, num_elevators +.5)
    ax.set_ylim(min_floor-.5, floors+.5)

    ax.set_xlabel('Elevator')
    #ax.set_ylabel('Floor')
    ax.set_title(f"Elevator System at time: {current_time}")
    ax.grid(False)

    ax.set_xticks(range(1, num_elevators+1))
    ax.set_yticks(range(min_floor, floors+1), [f"Floor {i}" for i in range(min_floor, floors+1)])
    ax.tick_params(length=0)
    for i in range(floors + 1):
        ax.axhline(y=i+.5, color='gray', linestyle='--', linewidth=0.9)

    for i in range(num_elevators + 1):
        ax.axvline(x=i+.5, color='black', linestyle='-', linewidth=0.9)

def update_elevator_positions():
    ax.cla()  # Clear the current axes
    setup_plot(ax)  # Reset the plot settings

    def horizontal_offset(i):
        return 0.1 + 0.05*(i+1)

    def add_elevator(ax, elevator_number, floor_number):
        # Define the size and position of the rectangle
        width = 0.2  # Width of the rectangle
        height = 1  # Height of the rectangle
        lower_left_x = elevator_number - width / 2
        lower_left_y = floor_number - height / 2

        # Create a rectangle and add it to the plot
        rect = Rectangle((lower_left_x, lower_left_y), width, height, color='black')
        ax.add_patch(rect)

    for i in range(num_elevators):
        elevator_positions[i] = elevator_positions_df.query(f'elevator=="E{i+1}" & time=={current_time}').location.values[0]
        add_elevator(ax, 1 + i, elevator_positions[i])
        
        #waiting 
        points_wating = passenger_positions_df.query(f'status=="W" & time == {current_time} & elevator=="E{i+1}"').location.values
        ax.plot([i+1 - horizontal_offset(0)]*len(points_wating), points_wating , 'ro', markersize=points_size)
        
        #Traveling 
        points_travel = passenger_positions_df.query(f'status=="T" & time == {current_time} & elevator=="E{i+1}"').location.values
        for j, p in enumerate(points_travel):
            ax.plot(i+1 - 0.02*(j+1), p , 'o', markersize=points_size, color = "white")

        #Done
        points_done = passenger_positions_df.query(f'status=="D" & time == {current_time} & elevator=="E{i+1}"').location.values
        ax.plot([i+1 + horizontal_offset(0)]*len(points_done), points_done , 'o', markersize=points_size, color = "green")


update_elevator_positions()
# Create slider for time control
axslider = plt.axes([0.25, 0.02, 0.65, 0.03])
slider = Slider(ax=axslider, label='Time', valmin=0, valmax=max_time, valinit=0, valstep=1)
slider.on_changed(slider_update)

# Add animation
ani = FuncAnimation(fig, auto_update, interval=500)

plt.show()
