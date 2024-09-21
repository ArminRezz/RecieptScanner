import os
import shutil
import argparse
import torch 
from reader import extract_text_from_image, parse_receipt_text, save_receipt_data
from readerV2 import extract_text_from_image as readerV2_extract, parse_receipt_text as readerV2_parse, save_receipt_data as readerV2_save
from transformers import DonutProcessor, VisionEncoderDecoderModel
from readerV3 import generate_text_from_image  # Adjust import as needed

# Set the device (GPU if available)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Load the processor and model
processor = DonutProcessor.from_pretrained("AdamCodd/donut-receipts-extract")
model = VisionEncoderDecoderModel.from_pretrained("AdamCodd/donut-receipts-extract")
model.to(device)

# from readerV3 import process_receipt as readerV3_process

# Usage:
# 1. To process all images in the directory using both readers:
#    python main.py
#
# 2. To process a specific image using both readers:
#    python main.py -i image_name.jpg
#
# 3. To process all images using a specific reader version:
#    python main.py -r v1
#    python main.py -r v2
#
# 4. To process a specific image using a specific reader version:
#    python main.py -i image_name.jpg -r v1
#    python main.py -i image_name.jpg -r v2

def process_single_image(image_path, output_dir, reader_version):
    if reader_version == 'v1':
        # Process with reader.py
        text = extract_text_from_image(image_path)
        receipt_data = parse_receipt_text(text)

        output_file = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(image_path))[0]}_reader_out.json')
        save_receipt_data(receipt_data, output_file)
        print(f"Receipt data saved for {os.path.basename(image_path)} using reader.py")

    elif reader_version == 'v2':
        # Process with readerV2.py
        text_v2 = readerV2_extract(image_path)
        receipt_data_v2 = readerV2_parse(text_v2)
        
        output_file_v2 = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(image_path))[0]}_readerV2_out.json')
        readerV2_save(receipt_data_v2, output_file_v2)
        print(f"Receipt data saved for {os.path.basename(image_path)} using readerV2.py")

    elif reader_version == 'v3':
        extracted_text = generate_text_from_image(model, image_path, processor, device)
        output_file = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(image_path))[0]}_readerV3_out.json')
        # Assuming you have a function to save the data
        save_receipt_data(extracted_text, output_file)
        print(f"Receipt data saved for {os.path.basename(image_path)} using readerV3.py")
    else:
        print(f"Invalid reader version: {reader_version}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process receipt images using OCR")
    parser.add_argument("-i", "--image", help="Name of a single image file to process (optional)")
    parser.add_argument("-r", "--reader", choices=['v1', 'v2', 'v3', 'both'], default='both',
                        help="Specify which reader version to use: v1, v2, v3, or both (default)")
    args = parser.parse_args()

    # Directory paths
    image_dir = r"C:\Users\arnoj\Documents\RecieptReader\recieptreader\images"
    output_dir = os.path.abspath(os.path.join(image_dir, "..", "output"))
    prev_output_dir = os.path.abspath(os.path.join(image_dir, "..", "prevoutputs"))

    # Create directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(prev_output_dir, exist_ok=True)

    # Move previous output files to prevoutputs folder
    for prev_output_file in os.listdir(output_dir):
        shutil.move(os.path.join(output_dir, prev_output_file), os.path.join(prev_output_dir, prev_output_file))

    def process_image(image_path):
        if args.reader == 'both':
            process_single_image(image_path, output_dir, 'v1')
            process_single_image(image_path, output_dir, 'v2')
            # process_single_image(image_path, output_dir, 'v3')
        else:
            process_single_image(image_path, output_dir, args.reader)

    if args.image:
        # Process only the specified image
        image_path = os.path.join(image_dir, args.image)
        if os.path.exists(image_path):
            process_image(image_path)
        else:
            print(f"Error: The specified image '{args.image}' does not exist in the images directory.")
    else:
        # Process all images in the directory
        for image_file in os.listdir(image_dir):
            if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(image_dir, image_file)
                process_image(image_path)

if __name__ == "__main__":
    main()