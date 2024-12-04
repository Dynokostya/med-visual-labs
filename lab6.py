import numpy as np
import matplotlib.pyplot as plt

# Завдання 1: Визначення тривимірних координат піксела
rows = 512
cols = 512
pixel_spacing = np.array([0.742188, 0.742188])
slice_thickness = 3.0
spacing_between_slices = 3.0
pixel_coordinates = (260, 203)

image_position_first_slice = np.array([-189.629, -217.216, -50.371])
image_orientation_first_slice = np.array([1.0, 0.0, 0.0, 0.0, 0.0, -1.0])

image_position_requested_slice = np.array([-189.629, -159.716, -50.371])
image_orientation_requested_slice = np.array([1.0, 0.0, 0.0, 0.0, 0.0, -1.0])

num_slices = 78
target_slice_index = 25

row_vector = image_orientation_requested_slice[:3]
col_vector = image_orientation_requested_slice[3:]
slice_vector = (image_position_requested_slice - image_position_first_slice) / spacing_between_slices

pixel_world_coords = (
    image_position_requested_slice +
    pixel_coordinates[0] * row_vector * pixel_spacing[0] +
    pixel_coordinates[1] * col_vector * pixel_spacing[1]
)

# Збереження тривимірних координат
output_coords_file = "output/lab_6_pixel_coordinates.txt"
with open(output_coords_file, "w") as f:
    f.write(f"3D Coordinates of the pixel: {pixel_world_coords}\n")

# Завдання 2: Візуалізація координатних осей та пікселя
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Відображення ізоцентру
ax.scatter(0, 0, 0, color='red', label='Isocenter')

# Відображення координатних осей
ax.quiver(0, 0, 0, 50, 0, 0, color='blue', label='X-axis')
ax.quiver(0, 0, 0, 0, 50, 0, color='green', label='Y-axis')
ax.quiver(0, 0, 0, 0, 0, 50, color='purple', label='Z-axis')

# Відображення площини томографічного зображення
x_plane = np.array([0, cols * pixel_spacing[0], cols * pixel_spacing[0], 0])
y_plane = np.array([0, 0, rows * pixel_spacing[1], rows * pixel_spacing[1]])
z_plane = np.zeros_like(x_plane) + target_slice_index * spacing_between_slices

ax.plot_trisurf(x_plane, y_plane, z_plane, color='lightgrey', alpha=0.5, label='Image Plane')

# Відображення положення пікселя
ax.scatter(*pixel_world_coords, color='black', label='Pixel Location')

ax.legend()
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z (mm)')

output_image_file = f"output/lab_6_visualization_slice_{target_slice_index}.png"
plt.savefig(output_image_file)
plt.close()

# Завдання 3: Генерація зображень під різними кутами
angles = [30, 60, 120, 180]
for angle in angles:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(0, 0, 0, color='red', label='Isocenter')
    ax.quiver(0, 0, 0, 50, 0, 0, color='blue', label='X-axis')
    ax.quiver(0, 0, 0, 0, 50, 0, color='green', label='Y-axis')
    ax.quiver(0, 0, 0, 0, 0, 50, color='purple', label='Z-axis')
    ax.plot_trisurf(x_plane, y_plane, z_plane, color='lightgrey', alpha=0.5)
    ax.scatter(*pixel_world_coords, color='black', label='Pixel Location')
    ax.view_init(30, angle)
    output_angle_file = f"output/lab_6_visualization_angle_{angle}.png"
    plt.savefig(output_angle_file)
    plt.close()
