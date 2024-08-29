import tkinter as tk

detected_levels = []
detected_bosses = []

def update_scoreboard(frame, levels, bosses):
    for widget in frame.winfo_children():
        widget.destroy()
    level_label = tk.Label(frame, text="Levels Detected:")
    level_label.pack()
    for level in levels:
        level_item = tk.Label(frame, text=level)
        level_item.pack()
    boss_label = tk.Label(frame, text="Bosses Detected:")
    boss_label.pack()
    for boss in bosses:
        boss_item = tk.Label(frame, text=boss)
        boss_item.pack()
