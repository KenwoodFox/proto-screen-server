import wifi
import socketpool
import ssl
import adafruit_requests
import os

def setup_wifi():
    """
    Connect to Wi-Fi using credentials from settings.toml.
    Returns:
        requests.Session: A session object for making HTTP requests.
    """
    ssid = os.getenv("CIRCUITPY_WIFI_SSID")
    password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

    if not ssid or not password:
        raise ValueError("Wi-Fi credentials not found in settings.toml")

    print(f"Connecting to Wi-Fi: {ssid}...")
    try:
        wifi.radio.connect(ssid, password)
        print(f"Connected to Wi-Fi: {wifi.radio.ipv4_address}")
    except Exception as e:
        print(f"Failed to connect to Wi-Fi: {e}")
        return None

    # Create a requests session
    print("Setting up HTTP session...")
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    return requests
