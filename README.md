# Receipt Reader 🧾

## Overview
Receipt Reader is an ongoing research project focused on accurately scanning grocery items and their corresponding prices from receipts into structured data. The primary goal is to develop an intuitive interface that enables roommates to easily split grocery bills.

## Current Implementation
The project includes three reader scripts and a collection of test receipt images:

1. **Reader Script 1**: Utilizes Optical Character Recognition (OCR) to extract text from receipts.
2. **Reader Script 2**: Currently not useful; serves as a testing framework.
3. **Reader Script 3**: Implements the AdamCodd DonutModel from Hugging Face, specifically designed for receipt data extraction in order to research how we could make our own model

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ReceiptReader.git
   cd ReceiptReader

2. Install the required packages:

   ```bash
   pip install -r requirements.txt

## Output 
Output will go to folder "output"
All previous outputs are moved to prevoutputs folder when new command is run

## Usage

To process all images in the directory using both readers:
   ```bash
   python main.py
   ```
To process a specific image using both readers:
   ```bash
   python main.py -i image_name.jpg
   ```

To process all images using a specific reader version:
   ```bash
   python main.py -r v1
   ```
To process a specific image using a specific reader version:
   ```bash
   python main.py -i image_name.jpg -r v1
   ```

## AdamCodd Donut Model For readerV3
This model has been retrained on an improved version of the **AdamCodd/donut-receipts** dataset (deduplicated, manually corrected). The new license for the V2 model is **cc-by-nc-4.0**. For commercial use rights, please contact him at [adamcoddml@gmail.com](mailto:adamcoddml@gmail.com). Meanwhile, the V1 model remains available under the **MIT license** (under the v1 branch).



## Issues
 - get the hugging face model working 
 - improve UI/UX
 - have data preprocessing
   - make sure images are named uniformly
   - images are black and white (should already be)
- have data post processing
   - text extraction output should be put into a excel sheet
- add Justin and Charles to github
- fix spelling erros
- don't use absolute paths and logins
- Have working draft by Oct 4th


