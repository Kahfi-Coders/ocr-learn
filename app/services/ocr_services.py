# ===== app/services/ocr_service.py =====
import pytesseract
from PIL import Image
import io
import cv2
import numpy as np
import hashlib

# (Optional) Set path to tesseract executable if on Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def preprocess_image(image_bytes):
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 🟡 Ganti threshold ke adaptive
    binary = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return Image.fromarray(binary)

def hash_bytes(data: bytes):
    return hashlib.md5(data).hexdigest()

async def run_ocr(file):
    await file.seek(0)
    image_bytes = await file.read()

    print("Image Hash: ", hash_bytes(image_bytes))

    image = preprocess_image(image_bytes)

    text = pytesseract.image_to_string(image, lang='eng')  # gunakan 'ind' untuk bahasa Indonesia
    return {
        "text": text,
        "debug_info": {
            "image_size": len(image_bytes),
            "image_mode": image.mode,
            "image_format": image.format,
            "image_name": file.filename
        }
    }