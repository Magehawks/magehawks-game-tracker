import threading
import time

class Timer(threading.Thread):
    def __init__(self, update_function):
        super().__init__()
        self.update_function = update_function
        self.daemon = True
        self.running = False
        self.paused = False
        self.start_time = None
        self.elapsed_time = 0

    def run(self):
        self.running = True
        self.paused = False
        self.start_time = time.time() - self.elapsed_time
        while self.running:
            if not self.paused:
                self.update_function()
                time.sleep(1)  # Update every second

    def start_timer(self):
        if not self.is_alive():
            self.start()  # Use the built-in start method to start the thread

    def pause_timer(self):
        if self.running and not self.paused:
            self.paused = True
            self.elapsed_time = time.time() - self.start_time

    def resume_timer(self):
        if self.running and self.paused:
            self.paused = False
            self.start_time = time.time() - self.elapsed_time

    def stop_timer(self):
        self.running = False
        self.paused = False

    def reset_timer(self):
        if self.is_alive():
            self.stop_timer()
        self.start_time = None
        self.elapsed_time = 0
        self.update_function()  # Update the timer display immediately
