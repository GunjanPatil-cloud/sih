try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except Exception as e:
    CV2_AVAILABLE = False
    print(f"[IMG] OpenCV not available: {e}")


def preprocess_image(image_path):
    """Full preprocessing pipeline for OCR.

    Steps:
    1. Read image
    2. Resize if too large
    3. Convert to grayscale
    4. Noise reduction (bilateral filter)
    5. Adaptive thresholding
    6. Contrast enhancement (CLAHE)

    Returns: preprocessed image (numpy array) or None on failure.
    """
    if not CV2_AVAILABLE:
        return None

    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"[IMG] Could not read image: {image_path}")
            return None

        # Resize if too large (keep aspect ratio, max 2000px wide)
        h, w = img.shape[:2]
        if w > 2000:
            scale = 2000 / w
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Noise reduction
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)

        # CLAHE for contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)

        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        return thresh

    except Exception as e:
        print(f"[IMG] Preprocessing error: {e}")
        return None


def preprocess_for_display(image_path):
    """Lighter preprocessing - just resize for display purposes."""
    if not CV2_AVAILABLE:
        return None
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None
        h, w = img.shape[:2]
        if w > 800:
            scale = 800 / w
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        return img
    except Exception:
        return None
