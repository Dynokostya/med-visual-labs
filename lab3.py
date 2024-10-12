import pydicom
import numpy as np
import ctypes
from PIL import Image, ImageDraw, ImageFont
import os

width, height = 0, 0
osmesa = ctypes.CDLL("libOSMesa.so")

OSMESA_RGBA = 0x1908
GL_UNSIGNED_BYTE = 0x1401

dicom_file = 'data/_DICOM_Image_for_Lab_2.dcm'
dicom_data = pydicom.dcmread(dicom_file)

pixel_data = dicom_data.pixel_array
height, width = pixel_data.shape

if np.max(pixel_data) > 255:
    pixel_data = (pixel_data / np.max(pixel_data)) * 255
pixel_data = pixel_data.astype(np.uint8)

buffer = np.zeros((width * height * 4,), dtype=np.uint8)

OSMesaCreateContext = osmesa.OSMesaCreateContext
OSMesaCreateContext.restype = ctypes.c_void_p
OSMesaCreateContext.argtypes = [ctypes.c_uint, ctypes.c_void_p]

OSMesaMakeCurrent = osmesa.OSMesaMakeCurrent
OSMesaMakeCurrent.restype = ctypes.c_int
OSMesaMakeCurrent.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint, ctypes.c_int, ctypes.c_int]

context = OSMesaCreateContext(OSMESA_RGBA, None)
if not OSMesaMakeCurrent(context, buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)), GL_UNSIGNED_BYTE, width, height):
    raise RuntimeError("OSMesa context creation failed!")

for y in range(height):
    for x in range(width):
        value = pixel_data[y, x]
        buffer[4 * (y * width + x): 4 * (y * width + x) + 3] = [value, value, value]
        buffer[4 * (y * width + x) + 3] = 255

study_time = dicom_data.StudyTime if 'StudyTime' in dicom_data else 'Unknown'

def overlay_study_time(buffer, width, height, text):
    font = ImageFont.load_default()
    
    img = Image.frombytes('RGBA', (width, height), buffer.tobytes())
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), f"Study Time: {text}", fill=(255, 0, 0, 255), font=font)
    
    img.save("output/lab3_with_text.png")

os.makedirs('output', exist_ok=True)

image = Image.frombytes('RGBA', (width, height), buffer.tobytes())
image.save("output/lab3.png")

user_input = input("Enter 'show' to overlay study time: ")
if user_input == 'show':
    overlay_study_time(buffer, width, height, study_time)

osmesa.OSMesaDestroyContext(context)
