import os
import shutil
import pytesseract
from PIL import Image
from modules.image_processing import preprocess_image

# Locate Tesseract binary (macOS Homebrew, Linux, standard paths)
TESSERACT_BIN = shutil.which('tesseract')
if not TESSERACT_BIN:
    for candidate in ['/opt/homebrew/bin/tesseract', '/usr/local/bin/tesseract', '/usr/bin/tesseract']:
        if os.path.exists(candidate):
            TESSERACT_BIN = candidate
            break
if TESSERACT_BIN:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_BIN


def extract_text(image_path):
    """Extract text from a product label image.

    Uses OpenCV preprocessing + Tesseract OCR.
    Falls back to raw image if preprocessing fails.

    Returns: dict with 'text' (extracted string) and 'confidence' (rough estimate).
    """
    text = ""

    # Try preprocessed image first (better accuracy)
    preprocessed = preprocess_image(image_path)
    if preprocessed is not None:
        try:
            # Convert numpy array back to PIL Image for pytesseract
            pil_img = Image.fromarray(preprocessed)
            text = pytesseract.image_to_string(pil_img, config='--psm 6')
        except Exception as e:
            print(f"[OCR] Preprocessed extraction failed: {e}")

    # Fallback: try raw image
    if not text.strip():
        try:
            text = pytesseract.image_to_string(Image.open(image_path), config='--psm 6')
        except Exception as e:
            print(f"[OCR] Raw extraction failed: {e}")
            return {'text': '', 'confidence': 0, 'error': str(e)}

    # Clean up OCR output
    cleaned = clean_ocr_text(text)

    # Rough confidence: based on how much readable text we got
    words = cleaned.split()
    confidence = min(95, max(10, len(words) * 3))

    return {
        'text': cleaned,
        'raw_text': text,
        'word_count': len(words),
        'confidence': confidence
    }


def clean_ocr_text(text):
    """Clean up common OCR artifacts."""
    if not text:
        return ""

    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        # Skip empty lines and lines that are just noise characters
        if not line:
            continue
        # Skip lines that are mostly special characters (OCR noise)
        alpha_count = sum(1 for c in line if c.isalnum() or c.isspace())
        if len(line) > 0 and alpha_count / len(line) < 0.3:
            continue
        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)
