import board
import digitalio
import time
import displayio

# Release any displays to free up pins
displayio.release_displays()

# === Pin Definitions ===
# RGB Pins (Upper and Lower rows)
R1 = digitalio.DigitalInOut(board.MTX_R1)
G1 = digitalio.DigitalInOut(board.MTX_G1)
B1 = digitalio.DigitalInOut(board.MTX_B1)
R2 = digitalio.DigitalInOut(board.MTX_R2)
G2 = digitalio.DigitalInOut(board.MTX_G2)
B2 = digitalio.DigitalInOut(board.MTX_B2)

# Address Pins (Row Selection)
ADDR_A = digitalio.DigitalInOut(board.MTX_ADDRA)
ADDR_B = digitalio.DigitalInOut(board.MTX_ADDRB)
ADDR_C = digitalio.DigitalInOut(board.MTX_ADDRC)

# Control Pins
CLK = digitalio.DigitalInOut(board.MTX_CLK)
LAT = digitalio.DigitalInOut(board.MTX_LAT)
OE = digitalio.DigitalInOut(board.MTX_OE)

# Set all pins as output
for pin in [R1, G1, B1, R2, G2, B2, ADDR_A, ADDR_B, ADDR_C, CLK, LAT, OE]:
    pin.direction = digitalio.Direction.OUTPUT

# === Utility Functions ===

def set_address(a, b, c):
    """Set row address (A, B, C pins)."""
    ADDR_A.value = a
    ADDR_B.value = b
    ADDR_C.value = c

def clock_pulse():
    """Send a single clock pulse."""
    CLK.value = True
    CLK.value = False

def latch_data():
    """Latch data into the matrix."""
    LAT.value = True
    LAT.value = False

def output_enable(state):
    """Enable or disable matrix output."""
    OE.value = not state  # OE is active-low

def clear_row():
    """Clear RGB data for a row."""
    R1.value = G1.value = B1.value = False
    R2.value = G2.value = B2.value = False
    for _ in range(16):  # Clear all columns
        clock_pulse()
    latch_data()

# === Manual Gradient ===

def manual_gradient():
    print("Starting manual gradient test...")
    output_enable(False)  # Disable display during setup

    for row in range(8):  # Test the first 8 rows
        print(f"Lighting Row {row}...")
        # Set address pins based on row binary
        set_address((row & 0b001) > 0, (row & 0b010) > 0, (row & 0b100) > 0)
        
        # Send pixel data for the row
        for col in range(128):
            R1.value = (col % 3 == 0)  # Red every 3rd pixel
            G1.value = (col % 3 == 1)  # Green every 3rd pixel
            B1.value = (col % 3 == 2)  # Blue every 3rd pixel

            R2.value = (col % 2 == 0)  # Alternate Red on bottom row
            G2.value = (col % 2 == 1)  # Alternate Green on bottom row
            B2.value = False  # No Blue on bottom

            clock_pulse()  # Move to the next pixel
            time.sleep(0.01)
        
            # Latch and display row data
            latch_data()
            output_enable(True)  # Enable display for a short time
        time.sleep(0.5)  # Display the row for 2s
        output_enable(False)  # Disable before moving to the next row
        clear_row()  # Clear row before moving on

    print("Manual gradient test complete.")

# === Main Execution ===

while True:
    manual_gradient()
    time.sleep(2)
