import torch
import re
import json
from PIL import Image
from transformers import pipeline

# still awaiting access from Mr AdamCodd to be able to use this one
    
# Use a pipeline as a high-level helper
pipe = pipeline("image-to-text", model="AdamCodd/donut-receipts-extract")

def extract_text_from_image(image_path):
    """
    Load an image and preprocess it for the model.
    """
    image = Image.open(image_path).convert("RGB")
    return image  # Return the image directly for the pipeline

def parse_receipt_text(image):
    """
    Generate text from the image using the pipeline.
    """
    # Use the pipeline to process the image
    result = pipe(image)
    decoded_text = result[0]['generated_text']  # Extract the generated text
    return processor.token2json(decoded_text)  # Assuming you still want to convert to JSON

def save_receipt_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# This function combines all steps and can be called from main.py
def process_receipt(image_path, output_path):
    image = extract_text_from_image(image_path)
    receipt_data = parse_receipt_text(image)
    save_receipt_data(receipt_data, output_path)