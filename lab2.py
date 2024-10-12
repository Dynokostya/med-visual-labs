import ctypes
import numpy as np
import math
from PIL import Image

width, height = 1024, 1024
buffer = np.zeros((width * height * 4,), dtype=np.uint8)

osmesa = ctypes.CDLL("libOSMesa.so")

OSMESA_RGBA = 0x1908
GL_UNSIGNED_BYTE = 0x1401

OSMesaCreateContext = osmesa.OSMesaCreateContext
OSMesaCreateContext.restype = ctypes.c_void_p
OSMesaCreateContext.argtypes = [ctypes.c_uint, ctypes.c_void_p]

OSMesaMakeCurrent = osmesa.OSMesaMakeCurrent
OSMesaMakeCurrent.restype = ctypes.c_int
OSMesaMakeCurrent.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint, ctypes.c_int, ctypes.c_int]

context = OSMesaCreateContext(OSMESA_RGBA, None)
if not OSMesaMakeCurrent(context, buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)), GL_UNSIGNED_BYTE, width, height):
    raise RuntimeError("OSMesa context creation failed!")

def draw_pixel(x, y):
    if 0 <= x < width and 0 <= y < height:
        buffer[4 * (y * width + x): 4 * (y * width + x) + 3] = [255, 255, 255]  # RGB (white)
        buffer[4 * (y * width + x) + 3] = 255  # Alpha channel (opaque)

def midpoint_circle_algorithm(center_x, center_y, radius):
    x = radius
    y = 0
    err = 0

    while x >= y:
        draw_pixel(center_x + x, center_y + y)
        draw_pixel(center_x + y, center_y + x)
        draw_pixel(center_x - y, center_y + x)
        draw_pixel(center_x - x, center_y + y)
        draw_pixel(center_x - x, center_y - y)
        draw_pixel(center_x - y, center_y - x)
        draw_pixel(center_x + y, center_y - x)
        draw_pixel(center_x + x, center_y - y)

        y += 1
        if err <= 0:
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1

def draw_axes():
    # Draw x-axis (horizontal axis along the bottom)
    for x in range(width):
        draw_pixel(x, height - 1)

    # Draw y-axis (vertical axis along the right side)
    for y in range(height):
        draw_pixel(width - 1, y)

def cartesian_to_cylindrical(x, y):
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return r, theta

def cylindrical_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

center_x = int(input("Enter the x-coordinate of the center (in pixels): "))
center_y = int(input("Enter the y-coordinate of the center (in pixels): "))
radius = int(input("Enter the radius of the circle (in pixels): "))

# Adjust center_x and center_y to match the origin in the bottom-right corner
center_x = width - center_x
center_y = height - center_y

# Draw the coordinate axes
draw_axes()

# Draw the circle in Cartesian coordinates
midpoint_circle_algorithm(center_x, center_y, radius)

# Example: Convert the circle's center to cylindrical coordinates and print the result
r, theta = cartesian_to_cylindrical(center_x - width, center_y - height)
print(f"Cylindrical coordinates of the center: r = {r}, theta = {theta}")

# Example: Convert back to Cartesian coordinates
x_cartesian, y_cartesian = cylindrical_to_cartesian(r, theta)
print(f"Converted back to Cartesian: x = {x_cartesian}, y = {y_cartesian}")

# Save the resulting image as PNG
image = Image.frombytes('RGBA', (width, height), buffer.tobytes())
image.save("output/lab2.png")

osmesa.OSMesaDestroyContext(context)
