# Firmware

The firmware is written mostly in micropython BUT the same
libs are also available from adafuit in cpp so it could
always be refactored.

The mpy code seems a little clunky, but this is just a prototype!
And it dosn't matter that much. I used PIO as a build system,
but really mpy dosn't need to be built. So im mostly
just leveraging it for lib management and packing the uf2 file
that the uf2 bootloader (installed by adafruit) expects.
