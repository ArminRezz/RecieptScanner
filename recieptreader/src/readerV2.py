import cv2
import pytesseract
import re
import json
import imutils
from imutils.perspective import four_point_transform

def extract_text_from_image(image_path):
    # Load the input image from disk, resize it, and compute the ratio
    orig = cv2.imread(image_path)
    image = orig.copy()
    image = imutils.resize(image, width=500)
    ratio = orig.shape[1] / float(image.shape[1])

    # Convert the image to grayscale, blur it slightly, and then apply edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
    edged = cv2.Canny(blurred, 75, 200)

    # Find contours in the edge map and sort them by size in descending order
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # Initialize a contour that corresponds to the receipt outline
    receiptCnt = None

    # Loop over the contours
    for c in cnts:
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # If our approximated contour has four points, then we can
        # assume we have found the outline of the receipt
        if len(approx) == 4:
            receiptCnt = approx
            break

    if receiptCnt is None:
        raise Exception("Could not find receipt outline. Try debugging your edge detection and contour steps.")

    # Apply a four-point perspective transform to the original image to
    # obtain a top-down bird's-eye view of the receipt
    receipt = four_point_transform(orig, receiptCnt.reshape(4, 2) * ratio)

    # Apply OCR to the receipt image
    options = "--psm 4"
    text = pytesseract.image_to_string(
        cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB),
        config=options)

    return text

def parse_receipt_text(text):
    # Define a regular expression that will match line items that include a price component
    pricePattern = r'([0-9]+\.[0-9]+)'
    
    items = []
    total = None
    tax = None

    # Loop over each of the line items in the OCR'd receipt
    for row in text.split("\n"):
        # Check to see if the price regular expression matches the current row
        if re.search(pricePattern, row) is not None:
            # If it's the total or tax line, extract that information
            if "TOTAL" in row.upper():
                total = re.search(pricePattern, row).group()
            elif "TAX" in row.upper():
                tax = re.search(pricePattern, row).group()
            else:
                # Otherwise, it's a regular item
                item_name = re.split(pricePattern, row)[0].strip()
                item_price = re.search(pricePattern, row).group()
                items.append((item_name, item_price))

    return {
        "items": items,
        "total": total,
        "tax": tax
    }

def save_receipt_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def process_receipt(image_path, output_path):
    text = extract_text_from_image(image_path)
    receipt_data = parse_receipt_text(text)
    save_receipt_data(receipt_data, output_path)