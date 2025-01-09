import wifi
import socketpool
import ssl
import adafruit_requests.adafruit_requests as adafruit_requests
import os
import time

# Get Wi-Fi credentials from settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

# Connect to Wi-Fi
print(f"Connecting to Wi-Fi: {ssid}...")
try:
    wifi.radio.connect(ssid, password)
    print(f"Connected! IP Address: {wifi.radio.ipv4_address}")
except Exception as e:
    print(f"Failed to connect to Wi-Fi: {e}")
    while True:
        time.sleep(1)  # Halt here if connection fails

# Set up HTTP requests
print("Setting up HTTP...")
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# Test GET Request
TEST_URL = "http://wifitest.adafruit.com/testwifi/index.html"

try:
    print(f"Fetching {TEST_URL}...")
    response = requests.get(TEST_URL)
    print("Response Text:")
    print(response.text)
    response.close()
except Exception as e:
    print(f"Failed to fetch URL: {e}")
