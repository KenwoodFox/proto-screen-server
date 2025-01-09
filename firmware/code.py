import time
import wifi_setup
import display_utils

# Setup Wi-Fi and HTTP session
requests = wifi_setup.setup_wifi()

if not requests:
    display_utils.show_error("Wi-Fi failed!")
    print("Wi-Fi setup failed. Halting...")
    while True:
        time.sleep(1)

# Main loop
API_ENDPOINT = "https://api.example.com/display-data"

while True:
    try:
        print(f"Fetching data from {API_ENDPOINT}...")
        response = requests.get(API_ENDPOINT)
        data = response.json()
        print("Response JSON:", data)

        # Process the data here
        # Example: display_utils.show_message(data["message"])

        response.close()
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        display_utils.show_error(error_message)

    # Wait before the next API call
    time.sleep(30)