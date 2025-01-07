import board
import displayio
import rgbmatrix
import framebufferio
import time

# Define matrix size and settings
scr_width = 128
scr_height = 16
bit_depth = 2  # Color depth (higher values = more colors, but slower refresh)

# Addressing Pins for ABCDE
addr_pins = [
    board.MTX_ADDRB,
    board.MTX_ADDRA,
    board.MTX_ADDRC,
]

# RGB Pins
rgb_pins = [
    board.MTX_R1,
    board.MTX_G1,
    board.MTX_B1,
    board.MTX_R2,
    board.MTX_G2,
    board.MTX_B2,
]

# Control Pins
clock_pin = board.MTX_CLK
latch_pin = board.MTX_LAT
oe_pin = board.MTX_OE

# Initialize RGB Matrix
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=scr_width,
    height=scr_height,
    bit_depth=bit_depth,
    rgb_pins=rgb_pins,
    addr_pins=addr_pins,
    clock_pin=clock_pin,
    latch_pin=latch_pin,
    output_enable_pin=oe_pin,
    tile=1,  # Single row of tiles
    serpentine=False,
)

# Attach framebuffer for display control
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

# Create a Display Group
splash = displayio.Group()
display.root_group = splash

# Create a bitmap for pixel control
pixel_bitmap = displayio.Bitmap(scr_width, scr_height, 2)  # 2 colors: on/off
pixel_palette = displayio.Palette(2)
pixel_palette[0] = 0x000000  # Black (Off)
pixel_palette[1] = 0xFFFFFF  # White (On)

# Add bitmap to display group
pixel_tile = displayio.TileGrid(pixel_bitmap, pixel_shader=pixel_palette, x=0, y=0)
splash.append(pixel_tile)


# Function to cycle pixels ON
def pixels_on():
    for y in range(scr_height):
        for x in range(scr_width):
            pixel_bitmap[x, y] = 1  # Turn pixel ON
            print(f"Enabling {x} and {y}")
            time.sleep(0.01)  # Small delay for visual effect


# Function to cycle pixels OFF
def pixels_off():
    for y in range(scr_height):
        for x in range(scr_width):
            pixel_bitmap[x, y] = 0  # Turn pixel OFF
            time.sleep(0.01)  # Small delay for visual effect

def test_address_lines():
    row_map = [
        (0, 0, 0),  # Row 0
        (0, 0, 1),  # Row 1
        (0, 1, 0),  # Row 2
        (0, 1, 1),  # Row 3
        (1, 0, 0),  # Row 4
        (1, 0, 1),  # Row 5
        (1, 1, 0),  # Row 6
        (1, 1, 1)   # Row 7
    ]

    for (a, b, c) in row_map:
        print(f"Addressing row: A={a}, B={b}, C={c}")
        for x in range(scr_width):
            pixel_bitmap[x, a * 4 + b * 2 + c] = 1  # Address row explicitly
        time.sleep(1)
        for x in range(scr_width):
            pixel_bitmap[x, a * 4 + b * 2 + c] = 0



# Main Loop
while True:
    # print("Cycling Pixels ON")
    # pixels_on()
    # time.sleep(1)  # Pause when fully lit

    # print("Cycling Pixels OFF")
    # pixels_off()
    # time.sleep(1)  # Pause when fully cleared
    test_address_lines()
