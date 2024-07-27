import numpy as np

# Coordinates of the parking boundary
boundary_coords = np.array([
    [9.7, 19.2],
    [27.2, 19.2],
    [27.2, 10.0],
    [9.7, 10.0]
])

# Coordinates of the pillars within the parking area
pillar_coords = [
    np.array([
        [11.7, 17.5],
        [12.5, 17.5],
        [12.5, 16.9],
        [11.7, 16.9]
    ]),
    np.array([
        [11.8, 12.0],
        [12.6, 12.0],
        [12.6, 11.4],
        [11.8, 11.4]
    ]),
    np.array([
        [24.3, 11.6],
        [25.1, 11.6],
        [25.1, 11.0],
        [24.3, 11.0]
    ]),
    np.array([
        [17.6, 11.6],
        [18.5, 11.6],
        [18.5, 11.0],
        [17.6, 11.0]
    ]),
    np.array([
        [17.6, 17.6],
        [18.5, 17.6],
        [18.5, 17.0],
        [17.6, 17.0]
    ]),
    np.array([
        [24.3, 17.6],
        [25.1, 17.6],
        [25.1, 17.0],
        [24.3, 17.0]
    ])
]

# Car dimensions and space required for the road
car_length = 5.0  # Example car length
car_width = 2.5   # Example car width
road_space = 1.0  # Space for the road

# Calculate parking lot length and width
x_coords = boundary_coords[:, 0]
y_coords = boundary_coords[:, 1]

parking_lot_length = np.max(x_coords) - np.min(x_coords)
parking_lot_width = np.max(y_coords) - np.min(y_coords)

# Add space for roads
parking_lot_length += 2 * road_space
parking_lot_width += 2 * road_space

# Calculate number of parking spots
num_cars_length = int(parking_lot_length / (car_length + road_space))
num_cars_width = int(parking_lot_width / (car_width + road_space))

# Initialize parking grid
parking_grid = np.zeros((num_cars_width, num_cars_length), dtype=int)

# Function to mark pillars in the parking grid
def mark_pillars(parking_grid, pillars, parking_lot_min_x, parking_lot_min_y, car_length, car_width, road_space):
    for pillar in pillars:
        min_x = np.min(pillar[:, 0])
        max_x = np.max(pillar[:, 0])
        min_y = np.min(pillar[:, 1])
        max_y = np.max(pillar[:, 1])

        # Convert pillar coordinates to grid indices
        start_row = int((min_y - parking_lot_min_y + road_space) / (car_width + road_space))
        end_row = int((max_y - parking_lot_min_y + road_space) / (car_width + road_space))
        start_col = int((min_x - parking_lot_min_x + road_space) / (car_length + road_space))
        end_col = int((max_x - parking_lot_min_x + road_space) / (car_length + road_space))

        # Mark the pillar area as occupied in the parking grid
        parking_grid[start_row:end_row+1, start_col:end_col+1] = 1

# Define parking lot min coordinates
parking_lot_min_x = np.min(x_coords)
parking_lot_min_y = np.min(y_coords)

# Mark the pillars in the parking grid
mark_pillars(parking_grid, pillar_coords, parking_lot_min_x, parking_lot_min_y, car_length, car_width, road_space)

# Calculate the number of available parking spots
available_parking_spots = np.sum(parking_grid == 0)

# Print the number of available parking spots
print(f"Number of available parking spots: {available_parking_spots}")

# Function to visualize the parking grid
def visualize_parking_grid(parking_grid, num_cars_length, num_cars_width):
    visualization = "+" + "-" * num_cars_length + "+\n"
    for row in parking_grid:
        visualization += "|"
        for cell in row:
            if cell == 0:
                visualization += "."
            else:
                visualization += "#"
        visualization += "|\n"
    visualization += "+" + "-" * num_cars_length + "+"
    return visualization

# Visualize the parking grid
visualization = visualize_parking_grid(parking_grid, num_cars_length, num_cars_width)
print("Close Parking Grid Visualization:")
print(visualization)
