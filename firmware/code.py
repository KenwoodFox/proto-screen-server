import time
import json

import wifi_setup
import fs_utils
import display_utils


# Setup Wi-Fi and HTTP session
requests = wifi_setup.setup_wifi()

if not requests:
    display_utils.show_error("Wi-Fi failed!")
    print("Wi-Fi setup failed. Halting...")
    while True:
        time.sleep(1)

# Constants
API_ENDPOINT = "https://led.kitsunehosting.net/api/checkin"
GIF_URL = "https://led.kitsunehosting.net/api/gifs/output.gif" # Can be grabbed!!!!
SETTINGS_PATH = "/settings.toml"

while True:
    try:
        print(f"Posting to {API_ENDPOINT}...")
        payload = {"screen_name": "example_screen"}  # Replace with actual screen name
        response = requests.post(API_ENDPOINT, json=payload)
        data = response.json()
        print("Response JSON:", data)

        # Save the offered_id to settings.toml
        if "offered_id" in data:
            fs_utils.save_to_file("screen_id", data["offered_id"])
            display_utils.scroll_text(f"ID now: {data['offered_id']}", 0x00FF00)

        # Download the GIF to memory
        gif_data = fs_utils.download_to_memory(GIF_URL, requests)
        if gif_data:
            # Display the GIF from memory
            display_utils.display_gif_from_memory(gif_data)
        else:
            display_utils.show_error("Failed to download GIF")

        response.close()
    except Exception as e:
        error_message = f"Error: {str(e)}"
        display_utils.show_error(error_message)
        

    # Wait before the next API call
    time.sleep(30)
