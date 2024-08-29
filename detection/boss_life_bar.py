import cv2
import numpy as np
from utils import save_screenshot

def detect_boss_life_bar(frame, boss_text_area, count, debug=False):
    x, y, w, h = boss_text_area
    bar_area = (x, y + h + 5, w, 40)  # Adjusted height for better detection
    bx, by, bw, bh = bar_area
    cropped_frame = frame[by:by+bh, bx:bx+bw]
    gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    if debug:
        save_screenshot(binary, f'binary_boss_life_bar_{count}.png')

    # Detect long rectangles that could be the boss life bar
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        cx, cy, cw, ch = cv2.boundingRect(cnt)
        if ch < 20 and cw > 200:  # Ensure detection of the long boss life bar
            cv2.rectangle(frame, (bx+cx, by+cy), (bx+cx+cw, by+cy+ch), (0, 0, 255), 2)
            if debug:
                save_screenshot(frame, f'boss_life_bar_detected_{count}.png')
            return True
    
    if debug:
        save_screenshot(frame, f'boss_life_bar_{count}_not_detected.png')
    return False
