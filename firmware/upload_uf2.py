# Patched together from other uf2 loader projects like the rp2040

Import("env", "projenv")

import shutil
import os

# Path to the UF2 file
UF2_PATH = "path/to/micropython.uf2"

def copy_uf2(target, source, env):
    print("Copying UF2 to MatrixPortal S3...")
    # Update this path to your mounted device (e.g., on Windows, macOS, or Linux)
    DEST_PATH = "/media/username/MATRIXPORTAL"
    if not os.path.exists(DEST_PATH):
        print(f"Error: {DEST_PATH} not found. Please connect the MatrixPortal S3.")
        return
    shutil.copy(UF2_PATH, DEST_PATH)
    print("UF2 copied successfully!")

env.AddPostAction("upload", copy_uf2)

