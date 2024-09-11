import unittest
from src.reader import extract_text_from_image, parse_receipt_text

class TestReceiptReader(unittest.TestCase):
    def test_extract_text_from_image(self):
        text = extract_text_from_image("images/receipt.jpg")
        self.assertIsInstance(text, str)

    def test_parse_receipt_text(self):
        text = """
        Apple $2.99
        Banana $1.29
        Orange Juice $3.49
        Total $7.77
        Tax $0.50
        """
        data = parse_receipt_text(text)
        self.assertIn("items", data)
        self.assertIn("total", data)
        self.assertIn("tax", data)

if __name__ == "__main__":
    unittest.main()