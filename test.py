import requests
import io
from PIL import Image
from IPython.display import display

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

image_bytes = query({
    "inputs": "Dog playing",
})

# Convert the image bytes to a PIL image
image = Image.open(io.BytesIO(image_bytes))

# Display the image
display(image)
