import cv2
import pytesseract
import numpy as np

def preprocess_boss_name_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return binary

def detect_boss_name(frame, boss_name_area, count, boss_names, debug=False):
    # Crop the boss name area from the frame
    x1, y1, x2, y2 = boss_name_area
    boss_name_image = frame[y1:y2, x1:x2]

    if boss_name_image.size == 0:
        print(f"Frame {count}: Boss name area cropping resulted in an empty image.")
        return "", False

    # Preprocess the image
    preprocessed_image = preprocess_boss_name_image(boss_name_image)

    # Perform OCR using Tesseract
    custom_config = r'--oem 3 --psm 6'
    detected_text = pytesseract.image_to_string(preprocessed_image, config=custom_config)

    if debug:
        cv2.imshow('Boss Name Detection', preprocessed_image)
        cv2.waitKey(1)

    for boss_name in boss_names:
        if boss_name.lower() in detected_text.lower():
            return boss_name, True

    return "", False
