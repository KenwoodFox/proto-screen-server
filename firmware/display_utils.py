import board
import displayio
from adafruit_matrixportal.adafruit_matrixportal.matrix import Matrix

# Initialize Matrix
scr_width = 64
scr_height = 32

matrix = Matrix(width=scr_width, height=scr_height)
display = matrix.display

# Setup Display Group
splash = displayio.Group()
display.root_group = splash  # Updated for CircuitPython 9.x

# Bitmap and Palette for the display
pixel_bitmap = displayio.Bitmap(scr_width, scr_height, 2)  # 2 colors: off/on
pixel_palette = displayio.Palette(2)
pixel_palette[0] = 0x000000  # Black (off)
pixel_palette[1] = 0xFFFFFF  # White (on)

# Add TileGrid to the display group
pixel_tile = displayio.TileGrid(pixel_bitmap, pixel_shader=pixel_palette, x=0, y=0)
splash.append(pixel_tile)

def show_message(message, x=0, y=0, color=1):
    """Display a message on the screen."""
    for i, char in enumerate(message):
        # Simulate characters as pixels (or replace with more advanced text later)
        pixel_bitmap[x + i, y] = color  # You could expand this to larger fonts
