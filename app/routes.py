import logging
from flask import Blueprint, request, jsonify
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the blueprint
main = Blueprint("main", __name__)

@main.route("/ocr", methods=["POST"])
def ocr():
    if "file" not in request.files:
        logging.error("No file part in the request.")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        logging.error("No selected file.")
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the PDF file
        logging.info("Processing PDF file for OCR.")
        pdf_file = file.read()
        pages = convert_from_bytes(pdf_file)

        text = ""
        for page_number, page in enumerate(pages, start=1):
            logging.info(f"Processing page {page_number} of PDF.")
            text += pytesseract.image_to_string(page)

        logging.info("OCR processing complete.")
        return jsonify({"text": text}), 200
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return jsonify({"error": str(e)}), 500


@main.route("/", methods=["GET", "POST", "HEAD"])
def home():
    if request.method == "GET":
        logging.info("GET request received at '/' route.")
        return """
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <title>Flask OCR App</title>
          </head>
          <body>
            <h1>Welcome to the Flask OCR App!</h1>
          </body>
        </html>
        """
    elif request.method == "POST":
        logging.info("POST request received at '/' route.")
        return jsonify({"message": "POST request received!"})
    elif request.method == "HEAD":
        logging.info("HEAD request received at '/' route.")
        return "", 200
