import cv2
import pytesseract
import json
from PIL import Image

# Page Segmentation Modes (PSM)
# 0: Orientation and script detection (OSD) only.
# 1: Automatic page segmentation with OSD.
# 2: Automatic page segmentation, but no OSD, or assume a single column of text of variable sizes.
# 3: Fully automatic page segmentation, but no OSD (default).
# 4: Assume a single column of text of uniform block size.
# 5: Assume a single uniform block of vertically aligned text.
# 6: Assume a single uniform block of text.
# 7: Treat the image as a single text line.
# 8: Treat the image as a single word.
# 9: Treat the image as a single character.
# 10: Treat the image as a single text line, but with OSD.

# OCR Engine Modes (OEM)
# 0: Original Tesseract only.
# 1: Neural nets LSTM only.
# 2: Tesseract + LSTM.
# 3: Default, based on what is available.
# You can set these modes in Tesseract using the --psm and --oem flags, respectively.

def extract_text_from_image(image_path):
    # Configuration for Tesseract OCR
    # --oem 1: Use LSTM neural network
    # --psm 6: Assume a single uniform block of text
    myconfig = r'--oem 1 --psm 6'

    # Open image using PIL
    image = Image.open(image_path) 

    # Convert to grayscale
    gray_image = image.convert('L')

    # Perform OCR on the grayscale image
    text = pytesseract.image_to_string(gray_image, config=myconfig)
    
    return text

def parse_receipt_text(text):
    # Simply print the OCR output
    print(text)
    return text

def save_receipt_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)