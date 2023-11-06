import requests
import json

def generate_image(description):
    """Generate an image based on a given description."""
    # Making an API call to generate an image
    # API_ENDPOINT would be the URL where you can POST the data to generate an image
    # API_KEY would be your authentication key
    try:
        response = requests.get(url=f"http://20.119.73.105:5000/image?prompt={description}")
        if response.status_code == 200:
            return json.dumps({"image_url": response.json()["image_url"]})
        else:
            return json.dumps({"error": "Failed to generate image"})
    except Exception as e:
        return json.dumps({"error": str(e)})
