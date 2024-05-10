import pytesseract
from PIL import ImageGrab

def find_text_on_screen(texts_by_language):
    screenshot = ImageGrab.grab()
    extracted_text = pytesseract.image_to_string(screenshot)

    for language, text in texts_by_language.items():
        if text in extracted_text:
            print(f"'{text}' button is there in {language}")
            return True
    return False

def check_for_text():
    start_button_language = {
        "English": "Confirm character",
        "German": "Akzeptieren"
    }
    return find_text_on_screen(start_button_language)
