import requests
import json
import time

# Configuration
CHECKIN_URL = "http://localhost:5000/api/checkin"
SCREEN_NAME = "Virtual_Screen"
SAVE_FILE = "virtual_screen_data.txt"


def save_data_to_file(data):
    """Save the received data to a file."""
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {SAVE_FILE}")
    except Exception as e:
        print(f"Failed to save data to file: {e}")


def load_data_from_file():
    """Load saved data from the file."""
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        print(f"Loaded data from {SAVE_FILE}: {data}")
        return data
    except FileNotFoundError:
        print(f"No existing data found in {SAVE_FILE}.")
        return None
    except Exception as e:
        print(f"Failed to load data from file: {e}")
        return None


def main():
    # Load existing data if available
    existing_data = load_data_from_file()
    if existing_data:
        print("Existing screen data found. Skipping checkin.")
        return

    # Simulate a checkin
    payload = {"screen_name": SCREEN_NAME}
    try:
        print(f"Sending checkin request to {CHECKIN_URL} with payload: {payload}")
        response = requests.post(CHECKIN_URL, json=payload)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Save the server response
        server_data = response.json()
        print(f"Received response from server: {server_data}")
        save_data_to_file(server_data)

    except requests.RequestException as e:
        print(f"Failed to check in with server: {e}")
    except json.JSONDecodeError:
        print("Failed to decode server response as JSON.")


if __name__ == "__main__":
    main()
