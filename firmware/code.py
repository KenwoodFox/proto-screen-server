import board
import displayio
import time

# Initialize display
from adafruit_matrixportal.adafruit_matrixportal.matrix import Matrix

scr_width = 128
scr_height = 64

# Setup Matrix with your resolution
matrix = Matrix(width=scr_width, height=scr_height)
display = matrix.display

# Create a Display Group
splash = displayio.Group()
display.root_group = splash  # Updated for CircuitPython 9.x

pixel_bitmap = displayio.Bitmap(scr_width, scr_height, 2)  # 2 colors: on/off
pixel_palette = displayio.Palette(2)
pixel_palette[0] = 0x000000  # Color 0: Black (Off)
pixel_palette[1] = 0xFFFFFF  # Color 1: White (On)

# Add bitmap to display group
pixel_tile = displayio.TileGrid(pixel_bitmap, pixel_shader=pixel_palette, x=0, y=0)
splash.append(pixel_tile)


# Function to cycle pixels ON
def pixels_on():
    for y in range(scr_height):
        for x in range(scr_width):
            pixel_bitmap[x, y] = 1  # Turn pixel ON
            time.sleep(0.001)  # Small delay for visual effect


# Function to cycle pixels OFF
def pixels_off():
    for y in range(scr_height):
        for x in range(scr_width):
            pixel_bitmap[x, y] = 0  # Turn pixel OFF
            time.sleep(0.001)  # Small delay for visual effect


# Main Loop
while True:
    print("Cycling Pixels ON")
    pixels_on()
    time.sleep(1)  # Pause when fully lit

    print("Cycling Pixels OFF")
    pixels_off()
    time.sleep(1)  # Pause when fully cleared
