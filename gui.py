from threading import Thread, Event
from main import main
from ttkbootstrap.constants import *
from shared import detected_levels, detected_bosses
import pygetwindow as gw
from game_tracker_app import GameTrackerApp

if __name__ == "__main__":
    app = GameTrackerApp()
    app.run()