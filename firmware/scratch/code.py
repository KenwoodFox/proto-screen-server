import board
import digitalio
import time
import displayio

# === Release Displays ===
displayio.release_displays()

# === Overall config ===
overall_width = 128
block_width = 32
overall_height = 64
block_height=16

# === Pin Definitions ===
# RGB Pins
R1 = digitalio.DigitalInOut(board.MTX_R1)
G1 = digitalio.DigitalInOut(board.MTX_G1)
B1 = digitalio.DigitalInOut(board.MTX_B1)
R2 = digitalio.DigitalInOut(board.MTX_R2)
G2 = digitalio.DigitalInOut(board.MTX_G2)
B2 = digitalio.DigitalInOut(board.MTX_B2)

# Address Pins
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
    print(f"Set row value {a},{b},{c}")
    ADDR_A.value = False
    ADDR_B.value = False
    ADDR_C.value = a

def clock_pulse():
    """Send a single clock pulse."""
    CLK.value = True
    time.sleep(0.001)
    CLK.value = False

def latch_data():
    """Latch data into the matrix."""
    LAT.value = True
    time.sleep(0.001)
    LAT.value = False

def output_enable(state):
    """Enable or disable matrix output."""
    OE.value = not state  # OE is active-low

def clear_display():
    """Clear all pixel data."""
    R1.value = G1.value = B1.value = False
    R2.value = G2.value = B2.value = False
    for _ in range(block_width):
        clock_pulse()
    latch_data()

# === Manual Row Shifting Test ===

def shift_row(row, color='white'):
    """Shift an entire row with a specific color."""
    print(f"Shifting Row {row}, Color: {color}")

    # Map row to binary address (A, B, C)
    set_address((row & 0b001) > 0, (row & 0b010) > 0, (row & 0b100) > 0)
    
    # Set RGB for the entire row
    if color == 'red':
        R1.value = True
        G1.value = B1.value = False
    elif color == 'green':
        G1.value = True
        R1.value = B1.value = False
    elif color == 'blue':
        B1.value = True
        R1.value = G1.value = False
    else:  # White as default
        R1.value = G1.value = B1.value = True

    # Shift the data out
    for _ in range(block_width/2):
        clock_pulse()

    # Latch and display row data
    latch_data()
    output_enable(True)
    time.sleep(1)  # Hold row for visibility
    output_enable(False)
    clear_display()

# === Main Execution ===
print("Manual Row Shift Test")
print("Shifting rows one by one with different colors...")

while True:
    for row in range(9):  # Test all 8 directly addressable rows
        shift_row(row, color='red' if (row%2==0) else 'blue')
    print("Row test cycle complete. Restarting in 2 seconds...")
    time.sleep(2)
