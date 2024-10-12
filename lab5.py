import pydicom
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import ctypes

# Mesa setup for off-screen rendering
osmesa = ctypes.CDLL("libOSMesa.so")

def load_dicom_image(file_path):
    dicom_data = pydicom.dcmread(file_path)
    return dicom_data.pixel_array, dicom_data

def display_image_with_labels(pixel_data):
    height, width = pixel_data.shape
    buffer = np.zeros((width * height * 4,), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            value = pixel_data[y, x]
            buffer[4 * (y * width + x): 4 * (y * width + x) + 3] = [value, value, value]
            buffer[4 * (y * width + x) + 3] = 255

    image = Image.frombytes('RGBA', (width, height), buffer.tobytes())
    image = image.resize((width * 2, height * 2))

    # Add labels "A", "L", and "Coronal plane"
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Adding labels "A" at the top
    draw.text((10, 10), "A", font=font, fill=(255, 255, 255, 255))
    # Adding labels "L" at the right side
    draw.text((width * 2 - 20, height), "L", font=font, fill=(255, 255, 255, 255))
    # Adding "Coronal plane" at the bottom
    draw.text((width * 2 - 120, height * 2 - 20), "Coronal plane", font=font, fill=(255, 255, 255, 255))

    image.save("output/lab5.png")

def calculate_3d_coordinates(x, y, dicom_data):
    image_position = dicom_data[0x0020, 0x0032].value
    pixel_spacing = dicom_data[0x0028, 0x0030].value
    orientation = dicom_data[0x0020, 0x0037].value
    
    x_spacing, y_spacing = pixel_spacing
    x_3d = image_position[0] + x_spacing * orientation[0] * x + y_spacing * orientation[3] * y
    y_3d = image_position[1] + x_spacing * orientation[1] * x + y_spacing * orientation[4] * y
    z_3d = image_position[2] + x_spacing * orientation[2] * x + y_spacing * orientation[5] * y
    
    return x_3d, y_3d, z_3d

def display_2d_and_3d_coordinates(x, y, dicom_data):
    x_3d, y_3d, z_3d = calculate_3d_coordinates(x, y, dicom_data)
    print(f"2D Coordinates: ({x}, {y})")
    print(f"3D Coordinates: ({x_3d}, {y_3d}, {z_3d})")

def main():
    dicom_file = 'data/_DICOM_Image_for_Lab_2.dcm'
    pixel_data, dicom_data = load_dicom_image(dicom_file)
    
    # Predefined pixel positions simulating mouse movement
    test_x, test_y = 100, 150
    
    # Display 2D and 3D coordinates
    display_2d_and_3d_coordinates(test_x, test_y, dicom_data)
    
    # Save the image with A, L, and Coronal plane labels
    display_image_with_labels(pixel_data)

main()
