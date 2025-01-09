import time
import board
import displayio
import terminalio

import adafruit_imageload

from io import BytesIO

from adafruit_matrixportal.matrix import Matrix
from adafruit_display_text import label


# Initialize the Matrix display
matrix = Matrix(width=64, height=32)  # Adjust dimensions to your screen
display = matrix.display

# Create a display group
splash = displayio.Group()
display.root_group = splash

def show_error(message):
    """Display an error message on the screen."""
    # Clear any existing content
    splash.pop() if len(splash) > 0 else None

    scroll_text(message, color=0xFF0000, speed=0.05)

def scroll_text(message, color=0xFFFFFF, speed=0.05):
    """
    Scroll a message horizontally across the screen.
    Args:
        message (str): The text to scroll.
        color (int): The color of the text.
        speed (float): Time delay between position updates.
    """
    # Clear any existing content
    splash.pop() if len(splash) > 0 else None

    # Create the text label
    text_area = label.Label(
        font=terminalio.FONT,
        text=message,
        color=color,
        x=64,
        y=16
    )
    splash.append(text_area)
    display.root_group = splash

    # Scroll text across the screen
    while text_area.x + text_area.bounding_box[2] > 0:  # Until the text is fully off-screen
        text_area.x -= 1  # Move text to the left
        time.sleep(speed)

def display_gif_from_memory(gif_data):
    """Display a GIF from in-memory binary data. (easier than sd storage)"""

    try:
        # Release any previous display groups
        display.root_group = None

        # Create a BytesIO stream from the binary data
        gif_stream = BytesIO(gif_data)
        gif_stream.seek(0)

        print(f"GIF size in memory: {len(gif_data)} bytes")

        # Load the GIF
        gif, palette = adafruit_imageload.load(
            gif_stream,
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )
        tile_grid = displayio.TileGrid(gif, pixel_shader=palette)

        # Create a display group and add the GIF
        group = displayio.Group()
        group.append(tile_grid)
        display.root_group = group

        print("Displaying GIF from memory")
    except Exception as e:
        print(f"Failed to display GIF: {e}")
        raise(e)