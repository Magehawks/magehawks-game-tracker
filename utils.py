import json
import os
import cv2

def load_json_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_screenshot(image, filename):
    os.makedirs("screenshots", exist_ok=True)
    filepath = os.path.join("screenshots", filename)
    cv2.imwrite(filepath, image)

def preprocess_image(image, resize_dim=(640, 480), grayscale=True):
    """
    Preprocess the image by resizing and converting to grayscale if needed.
    """
    if resize_dim:
        image = cv2.resize(image, resize_dim)
    if grayscale:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image
