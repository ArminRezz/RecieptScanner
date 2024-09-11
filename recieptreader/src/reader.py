import cv2
import pytesseract
import re
import json

def extract_text_from_image(image_path):
    # Load image using OpenCV
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is not None:
        # Convert the image to RGB format (required by pytesseract)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image_rgb)
        return text
    else:
        print("Error: Unable to load the image.")
        return ""

def parse_receipt_text(text):
    # Regex to find items and prices
    item_pattern = r'(\w+(?: \w+)*) \$(\d+\.\d{2})'
    total_pattern = r'Total \$(\d+\.\d{2})'
    tax_pattern = r'Tax \$(\d+\.\d{2})'

    # Find all items and prices
    items = re.findall(item_pattern, text)
    total_match = re.search(total_pattern, text)
    total = total_match.group(1) if total_match else None
    tax_match = re.search(tax_pattern, text)
    tax = tax_match.group(1) if tax_match else None

    return {
        "items": items,
        "total": total,
        "tax": tax
    }

def save_receipt_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)