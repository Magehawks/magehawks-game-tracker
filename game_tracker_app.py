import webbrowser
import customtkinter
from customtkinter import *
from game_config_manager import GameConfigManager

class GameTrackerApp:
    def __init__(self):
        self.root = CTk()
        self.root.geometry("800x600")
        self.root.title("Magehawks game tracker tool")
        self.root.resizable(False, False)

        self.menu_frame = CTkFrame(master=self.root, fg_color="light gray")
        self.menu_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.menu_bottom_frame = CTkFrame(self.menu_frame, fg_color="light gray")
        self.menu_bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.menu_settings_frame = CTkFrame(self.root, fg_color="white")
        self.menu_settings_frame.pack(side=RIGHT, expand=True, fill=BOTH)

        self.last_config_path = GameConfigManager.load_last_game_config()
        self.game_image_in_menu_frame = GameConfigManager.load_game_icon(self.last_config_path)
        self.game_image_label = CTkLabel(self.menu_frame, image=self.game_image_in_menu_frame, text="")
        self.game_image_label.pack()

        self.create_menu_buttons()
        self.create_bottom_buttons()

    def create_menu_buttons(self):
        CTkButton(self.menu_frame, text="Game Settings", command=lambda: self.update_menu_settings("Game")).pack(pady=10)
        CTkButton(self.menu_frame, text="Time Tracker", command=lambda: self.update_menu_settings("TimeTracker")).pack(pady=10)
        CTkButton(self.menu_frame, text="Time Video Tracker", command=lambda: self.update_menu_settings("TimeVideoTracker")).pack(pady=10)
        CTkButton(self.menu_frame, text="Video Comparison", command=lambda: self.update_menu_settings("VideoComparsion")).pack(pady=10)

    def create_bottom_buttons(self):
        CTkButton(self.menu_bottom_frame, text="GeneralSettings", width=10, height=10).pack(side=LEFT, pady=10, padx=10)
        CTkButton(self.menu_bottom_frame, text="Discord", width=10, height=10).pack(side=LEFT, pady=10, padx=10)
        CTkButton(self.menu_bottom_frame, text="Patreon", width=10, height=10).pack(side=LEFT, pady=10, padx=10)
        CTkButton(self.menu_bottom_frame, text="GitHub", command=lambda: webbrowser.open("https://github.com/Magehawks/magehawks-game-tracker"), width=10, height=10).pack(side=LEFT, pady=10, padx=10)

    def update_menu_settings(self, content_type):
        for widget in self.menu_settings_frame.winfo_children():
            widget.destroy()

        if content_type == "Game":
            CTkLabel(self.menu_settings_frame, text="Game Settings").pack()
            CTkButton(self.menu_settings_frame, text="Add New List", command=self.add_new_list_view).pack(pady=10)
        elif content_type == "TimeTracker":
            CTkLabel(self.menu_settings_frame, text="Time Tracker Settings").pack()
            CTkButton(self.menu_settings_frame, text="Start Time Tracker").pack()
        elif content_type == "TimeVideoTracker":
            CTkLabel(self.menu_settings_frame, text="Time Video Tracker Settings").pack()
            CTkButton(self.menu_settings_frame, text="Start Time Video Tracker").pack()
        elif content_type == "VideoComparsion":
            CTkLabel(self.menu_settings_frame, text="Video Comparison Settings").pack()
            CTkButton(self.menu_settings_frame, text="Start Video Comparison").pack()

    def add_new_list_view(self):
        for widget in self.menu_settings_frame.winfo_children():
            widget.destroy()

        CTkLabel(self.menu_settings_frame, text="Enter Level Names or Bosses").pack()
        entry_list = []

        def add_entry():
            entry = CTkEntry(self.menu_settings_frame)
            entry.pack(pady=5)
            entry_list.append(entry)

        def save_list():
            game_name = "darksouls_remastered"  # Replace with actual game name from config
            os.makedirs(f"GameHistory/{game_name}", exist_ok=True)
            with open(f"GameHistory/{game_name}/levels_or_bosses.txt", "w") as file:
                for entry in entry_list:
                    file.write(entry.get() + "\n")
            self.update_menu_settings("Game")

        CTkButton(self.menu_settings_frame, text="Add Entry", command=add_entry).pack(pady=10)
        CTkButton(self.menu_settings_frame, text="Save List", command=save_list).pack(pady=10)

    def run(self):
        self.root.mainloop()