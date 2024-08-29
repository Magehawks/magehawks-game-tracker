import cv2
import pytesseract
from utils import preprocess_image, save_screenshot

def detect_level_text(frame, area, count, level_names, debug=False):
    x, y, w, h = area
    cropped_frame = frame[y:y+h, x:x+w]
    binary = preprocess_image(cropped_frame)
    if debug:
        save_screenshot(binary, f'binary_level_text_{count}.png')

    config = '--psm 8'
    text = pytesseract.image_to_string(binary, config=config)
    detected_text = text.strip()

    if debug:
        print(f"Detected level text: {detected_text}")

    for level_name in level_names:
        if level_name.lower() in detected_text.lower():
            return level_name, True

    return "", False
