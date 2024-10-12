import pydicom
import numpy as np
import ctypes
from PIL import Image

osmesa = ctypes.CDLL("libOSMesa.so")

OSMESA_RGBA = 0x1908
GL_UNSIGNED_BYTE = 0x1401

def load_dicom_image(file_path):
    dicom_data = pydicom.dcmread(file_path)
    return dicom_data

def get_pixel_data(dicom_data):
    pixel_data = dicom_data.pixel_array
    intercept = dicom_data.get((0x0028, 0x1052), 6.860).value
    slope = dicom_data.get((0x0028, 0x1053), 0.013325).value
    return pixel_data, slope, intercept

def apply_linear_transform(pixel_data, slope, intercept):
    return pixel_data * slope + intercept

def clamp_pixel_values(pixel_data, min_val, max_val):
    pixel_data[pixel_data > max_val] = max_val
    pixel_data[pixel_data < min_val] = min_val
    return pixel_data

def reset_image(dicom_data):
    return dicom_data.pixel_array

def display_image(buffer, width, height):
    image = Image.frombytes('RGBA', (width, height), buffer.tobytes())
    image.save("output/lab4.png")

def save_modified_dicom(dicom_data, new_pixel_data, file_name):
    dicom_data.PixelData = new_pixel_data.tobytes()
    dicom_data.save_as(file_name)

def display_pixel_data_info(pixel_data, slope, intercept, dicom_data):
    print(f"Min Pixel Value: {np.min(pixel_data)}")
    print(f"Max Pixel Value: {np.max(pixel_data)}")
    print(f"Slope: {slope}")
    print(f"Intercept: {intercept}")
    print(f"Pixel Data Type: {pixel_data.dtype}")
    if (0x0008, 0x0008) in dicom_data:
        print(f"Image Type: {dicom_data[(0x0008, 0x0008)].value}")

dicom_file = 'data/_DICOM_Image_for_Lab_2.dcm'
dicom_data = load_dicom_image(dicom_file)

pixel_data, slope, intercept = get_pixel_data(dicom_data)
height, width = pixel_data.shape

original_pixel_data = np.copy(pixel_data)

display_pixel_data_info(pixel_data, slope, intercept, dicom_data)

user_input = input("Choose an event: 1 for linear transform, 2 for clamping, 3 for both, 4 to reset: ")

if user_input == '1':
    pixel_data = apply_linear_transform(pixel_data, slope, intercept)
elif user_input == '2':
    min_val = 25
    max_val = 190
    pixel_data = clamp_pixel_values(pixel_data, min_val, max_val)
elif user_input == '3':
    pixel_data = apply_linear_transform(pixel_data, slope, intercept)
    pixel_data = clamp_pixel_values(pixel_data, 25, 190)
elif user_input == '4':
    pixel_data = reset_image(dicom_data)

buffer = np.zeros((width * height * 4,), dtype=np.uint8)
for y in range(height):
    for x in range(width):
        value = pixel_data[y, x]
        buffer[4 * (y * width + x): 4 * (y * width + x) + 3] = [value, value, value]
        buffer[4 * (y * width + x) + 3] = 255

display_image(buffer, width, height)

if user_input in ['1', '2', '3']:
    save_modified_dicom(dicom_data, pixel_data, f'output/lab4_dicom{user_input}.dcm')
