import time
import board
import displayio
import terminalio

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