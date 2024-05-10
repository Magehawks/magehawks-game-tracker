import tkinter as tk
from tkinter import ttk
from config_loader import ConfigLoader
import pygetwindow as gw
from timer import Timer
import time

class GameTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Tracker")
        
        self.loader = ConfigLoader()
        self.config = None

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.frame, text="Select a game:").grid(row=0, column=0, sticky=tk.W)
        self.game_var = tk.StringVar()
        self.game_menu = ttk.Combobox(self.frame, textvariable=self.game_var, values=self.loader.config_files, state='readonly')
        self.game_menu.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.game_menu.bind("<<ComboboxSelected>>", self.load_selected_game)

        self.timer_label = ttk.Label(self.frame, text="00:00:00", font=('Helvetica', 18))
        self.timer_label.grid(row=1, column=1, sticky=tk.W)

        self.start_timer_button = ttk.Button(self.frame, text="Start Timer", command=self.start_timer)
        self.start_timer_button.grid(row=2, column=1, sticky=tk.W)

        self.pause_timer_button = ttk.Button(self.frame, text="Pause Timer", command=self.pause_timer)
        self.pause_timer_button.grid(row=3, column=1, sticky=tk.W)

        self.resume_timer_button = ttk.Button(self.frame, text="Resume Timer", command=self.resume_timer)
        self.resume_timer_button.grid(row=4, column=1, sticky=tk.W)

        self.stop_timer_button = ttk.Button(self.frame, text="Stop Timer", command=self.stop_timer)
        self.stop_timer_button.grid(row=5, column=1, sticky=tk.W)

        self.reset_timer_button = ttk.Button(self.frame, text="Reset Timer", command=self.reset_timer)
        self.reset_timer_button.grid(row=6, column=1, sticky=tk.W)

        self.status_label = ttk.Label(self.frame, text="Status: Not running", font=('Helvetica', 12))
        self.status_label.grid(row=7, column=1, sticky=tk.W)

        self.start_detect_button = ttk.Button(self.frame, text="Start Detecting", command=self.start_detecting)
        self.start_detect_button.grid(row=8, column=1, sticky=tk.W)

        self.stop_detecting_button = ttk.Button(self.frame, text="Stop Detecting", command=self.stop_detecting)
        self.stop_detecting_button.grid(row=9, column=2, sticky=tk.W)

        self.start_tracking_button = ttk.Button(self.frame, text="Start Tracking", command=self.start_tracking, state='disabled')
        self.start_tracking_button.grid(row=10, column=1, sticky=tk.W)

        self.timer = None  # Initialize timer as None

    def start_timer(self):
        if not self.timer or not self.timer.is_alive():
            self.timer = Timer(self.update_timer_label)
            self.timer.start_timer()

    def update_timer_label(self):
        """Update the timer label with the elapsed time."""
        if self.timer and self.timer.running and not self.timer.paused:
            elapsed_time = int(time.time() - self.timer.start_time)
            formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
            self.timer_label.config(text=formatted_time)
            self.timer_label.after(1000, self.update_timer_label)  # Schedule the next update

    def pause_timer(self):
        if self.timer:
            self.timer.pause_timer()

    def resume_timer(self):
        if self.timer and self.timer.paused:
            self.timer.resume_timer()

    def stop_timer(self):
        if self.timer:
            self.timer.stop_timer()

    def reset_timer(self):
        if self.timer:
            self.timer.reset_timer()
            self.timer_label.config(text="00:00:00")  # Reset display

    def load_selected_game(self, event=None):
        game_key = self.game_var.get()
        self.config = self.loader.load_config(game_key)

    def start_detecting(self):
        # Start or resume game status detection
        if not hasattr(self, 'game_status_detector') or not self.game_status_detector.is_alive():
            self.game_status_detector = Timer(self.check_game_status)
            self.game_status_detector.start_timer()

    def stop_detecting(self):
        # Stop game status detection
        if hasattr(self, 'game_status_detector') and self.game_status_detector.is_alive():
            self.game_status_detector.stop_timer()
            self.status_label.config(text="Detection stopped.", foreground="black")

    def check_game_status(self):
        if self.config:
            try:
                game_windows = gw.getWindowsWithTitle(self.config['window_title'])
                if not game_windows:
                    self.update_status(f"The game '{self.config['game_title']}' is not running", "red")
                    self.start_tracking_button.config(state='disabled')
                    return

                # Find the actual game window by a more specific attribute, if necessary
                game_window = None
                for win in game_windows:
                    # Example additional check - adapt as necessary based on your needs
                    if "specific attribute or condition" in win.title:
                        game_window = win
                        break

                if game_window is None:
                    game_window = game_windows[0]  # Fallback if no specific window is identified

                # Debug output
                print(f"Window Title: {game_window.title}, is Active: {game_window.isActive}")

                if game_window.isActive:
                    self.update_status(f"Game '{self.config['game_title']}' is Active and Focused", "green")
                    self.start_tracking_button.config(state='normal')
                else:
                    self.update_status(f"The game '{self.config['game_title']}' is running but not focused", "yellow")
                    self.start_tracking_button.config(state='normal')
            except Exception as e:
                print(f"Error checking game status: {e}")
                self.update_status("Error in checking game status.", "red")

    def update_status(self, message, color):
        self.status_label.config(text=message, foreground=color)

    def start_tracking(self):
        """Function to start tracking game events."""
        # Placeholder for event detection logic
        if self.detect_accepted_event():
            #self.start_timer()
            print(f"get tracked")
 
    def detect_accepted_event(self):
        """Detect if the 'Accepted' button in the game has been clicked."""
        # Implement the logic to detect the in-game event.
        # This might involve scanning the screen, reading logs, or other methods depending on the game and what's possible.
        # Return True if the event is detected, False otherwise.
        return True  # Placeholder, return True for testing
