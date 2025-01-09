import json

CONFIG_PATH = "/data/config.json"

def save_to_file(key, value, file_path=CONFIG_PATH):
    """Save a key-value pair to a writable JSON file."""

    return # Not implemented!

    try:
        # Try reading existing data
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
        except (OSError, ValueError):
            config = {}  # File doesn't exist or is invalid; create new dict

        # Update the key-value pair
        config[key] = value

        # Write back to the file
        with open(file_path, "w") as f:
            json.dump(config, f)
        print(f"Saved '{key} = {value}' to {file_path}")
    except Exception as e:
        print(f"Failed to save to {file_path}: {e}")
        display_utils.show_error("Save failed!")

def save_file_from_url(url, file_path, requests):
    """Download a file from a URL and save it to a given path."""
    try:
        print(f"Downloading from {url}...")
        response = requests.get(url, stream=True)

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        print(f"Saved to {file_path}")
        response.close()
        return True
    except Exception as e:
        print(f"Failed to download file: {e}")
        return False

def download_to_memory(url, requests):
    """Download a file from a URL into memory."""
    try:
        print(f"Downloading from {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            return response.content  # Return the binary content
        else:
            print(f"Failed to download: {response.status_code}")
            return None
    except Exception as e:
        print(f"Failed to download file: {e}")
        return None
