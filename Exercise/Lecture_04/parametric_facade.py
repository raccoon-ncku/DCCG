import compas.geometry as cg
from compas_viewer import Viewer

# === CONFIGURATION ===
GRID_SIZE_X = 15
GRID_SIZE_Z = 10
GRID_STEP = 1.2
ATTRACTION_POINT = cg.Point(9.0, 0, 6.0)
MAX_Y_DISPLACEMENT = 3.0
MAX_ATTRACTION_DISTANCE = 20.0

# === VIEWER SETUP ===
viewer = Viewer()

# === MAIN GENERATION LOOP ===
for x in range(GRID_SIZE_X):
    for z in range(GRID_SIZE_Z):
        
        # Position calculation
        base_point = cg.Point(x * GRID_STEP, 0, z * GRID_STEP)
        
        # Attraction-based Y displacement
        attraction_vector = cg.Vector(base_point.x, 0, base_point.z) - cg.Vector(ATTRACTION_POINT.x, 0, ATTRACTION_POINT.z)
        attraction_distance = attraction_vector.length
        normalized_attraction = max(0, 1.0 - (attraction_distance / MAX_ATTRACTION_DISTANCE))
        attraction_strength = normalized_attraction ** 2
        y_displacement = attraction_strength * MAX_Y_DISPLACEMENT
        current_point = cg.Point(base_point.x, y_displacement, base_point.z)
        
        # Size calculation
        x_factor = x / (GRID_SIZE_X - 1)
        z_factor = z / (GRID_SIZE_Z - 1)
        y_factor = y_displacement / MAX_Y_DISPLACEMENT
        position_factor = (x_factor + z_factor) / 2.0
        size_from_position = 0.3 + position_factor * 0.4
        displacement_factor = 1.0 + y_factor * 0.5
        box_size = size_from_position * displacement_factor
        
        # Rotation calculation
        rotation_x = x_factor * 0.8 - 0.4
        rotation_y = z_factor * 0.6 - 0.3
        rotation_z = y_factor * 0.5
        
        # Box creation and display
        frame = cg.Frame(current_point, [1, rotation_x, rotation_y], [rotation_z, 0.1, 0.3])
        box = cg.Box(box_size, box_size, box_size, frame=frame)
        viewer.scene.add(box, name=f"Panel_{x}_{z}")

# === DISPLAY ===
viewer.show()