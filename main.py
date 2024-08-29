import cv2
from threading import Event, Thread
from PIL import Image, ImageTk
from utils import load_json_config
from shared import update_scoreboard, detected_levels, detected_bosses
from detection.level_text import detect_level_text
from detection.boss_name import detect_boss_name
import time

def main(video_path, config_path, stop_event, scoreboard_frame, capture_mode, video_label, is_paused, debug=False):
    config = load_json_config(config_path)
    level_text_area = tuple(config['level_text_area'])
    boss_name_area = tuple(config['boss_name_area'])
    boss_names = config['boss_names']
    level_names = config['level_names']
    game_window_name = config['game_window_name']

    if capture_mode == "video":
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Unable to open video file {video_path}")
            return

        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        count = 0
        max_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        last_detection_times = {'level': None, 'boss': None}

        while cap.isOpened() and count < max_frames and not stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            if count % 2 == 0:
                current_time = time.time()

                # Level name detection
                new_level_text, new_area_detected = detect_level_text(frame, level_text_area, count, level_names, debug)
                if new_area_detected and (last_detection_times['level'] is None or current_time - last_detection_times['level'] > 60):
                    print(f"Frame {count}: Detected level text: '{new_level_text}'")
                    detected_levels.append(new_level_text)
                    update_scoreboard(scoreboard_frame, detected_levels, detected_bosses)
                    last_detection_times['level'] = current_time

                # Boss name detection
                new_boss_name, new_boss_detected = detect_boss_name(frame, boss_name_area, count, boss_names, debug)
                if new_boss_detected and (last_detection_times['boss'] is None or current_time - last_detection_times['boss'] > 60):
                    print(f"Frame {count}: Detected boss name: '{new_boss_name}'")
                    detected_bosses.append(new_boss_name)
                    update_scoreboard(scoreboard_frame, detected_levels, detected_bosses)
                    last_detection_times['boss'] = current_time

                # Update the video display label in the GUI
                if not is_paused.is_set():
                    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    imgtk = ImageTk.PhotoImage(image=img)
                    video_label.imgtk = imgtk  # Keep a reference to avoid garbage collection
                    video_label.config(image=imgtk)

            while is_paused.is_set():
                time.sleep(0.1)

            count += 1

        cap.release()
        cv2.destroyAllWindows()

    elif capture_mode == "game":
        # Implement game mode handling here
        pass

if __name__ == "__main__":
    from tkinter import Tk, Frame, Label
    import tkinter as tk

    # Initialize Tkinter
    root = Tk()
    root.title("Video Display")

    # Create a frame for scoreboard (you can adjust the layout as needed)
    scoreboard_frame = Frame(root)
    scoreboard_frame.pack()

    # Create a label for displaying video
    video_label = Label(root)
    video_label.pack()

    # Define your configuration and video path (adjust as needed)
    config_path = "configs/config_darksouls.json"
    video_path = "path/to/your/video.mp4"  # Replace with your video file path

    # Create stop event and is_paused event for controlling video playback
    stop_event = Event()
    is_paused = Event()

    # Create a thread for running main function (to avoid blocking the GUI)
    thread = Thread(target=main, args=(video_path, config_path, stop_event, scoreboard_frame, "video", video_label, is_paused))
    thread.start()

    # Run the Tkinter main loop
    root.mainloop()

    # Clean up after closing Tkinter window
    stop_event.set()
    thread.join()
