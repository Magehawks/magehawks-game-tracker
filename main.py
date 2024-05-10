from tkinter import Tk
from game_tracker_gui import GameTrackerApp
from text_recognition import check_for_text

def main():
    root = Tk()
    app = GameTrackerApp(root)
    
    # Example usage of check_for_text
    if check_for_text():
        print("Text detected!")

    root.mainloop()

if __name__ == "__main__":
    main()