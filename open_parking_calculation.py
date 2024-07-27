import numpy as np

# Coordinates of the parking boundary
boundary_coords = np.array([
    [5.5, 22.8],
    [35.4, 22.8],
    [35.4, 4.4],
    [5.5, 4.4]
])

# Coordinates of the buildings within the parking area
building_coords = [
    np.array([
        [9.7, 19.2],
        [27.2, 19.2],
        [27.2, 10.0],
        [9.7, 10.0]
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

# Function to mark buildings in the parking grid
def mark_buildings(parking_grid, buildings, parking_lot_min_x, parking_lot_min_y, car_length, car_width, road_space):
    for building in buildings:
        min_x = np.min(building[:, 0])
        max_x = np.max(building[:, 0])
        min_y = np.min(building[:, 1])
        max_y = np.max(building[:, 1])

        # Convert building coordinates to grid indices
        start_row = int((min_y - parking_lot_min_y + road_space) / (car_width + road_space))
        end_row = int((max_y - parking_lot_min_y + road_space) / (car_width + road_space))
        start_col = int((min_x - parking_lot_min_x + road_space) / (car_length + road_space))
        end_col = int((max_x - parking_lot_min_x + road_space) / (car_length + road_space))

        # Mark the building area as occupied in the parking grid
        parking_grid[start_row:end_row+1, start_col:end_col+1] = 1

# Define parking lot min coordinates
parking_lot_min_x = np.min(x_coords)
parking_lot_min_y = np.min(y_coords)

# Mark the buildings in the parking grid
mark_buildings(parking_grid, building_coords, parking_lot_min_x, parking_lot_min_y, car_length, car_width, road_space)

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
print("Open Parking Grid Visualization:")
print(visualization)
