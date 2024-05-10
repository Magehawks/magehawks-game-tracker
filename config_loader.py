import json
import os

class ConfigLoader:
    def __init__(self, config_directory="config"):
        self.config_directory = config_directory
        self.config_files = self.scan_config_directory()

    def scan_config_directory(self):
        config_files = []
        for filename in os.listdir(self.config_directory):
            if filename.endswith("_config.json"):
                # Just store the root part of the filename to avoid repetition
                config_files.append(filename.replace("_config.json", ""))
        return config_files

    def load_config(self, game_key):
        config_file = os.path.join(self.config_directory, f'{game_key}_config.json')
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_file}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Could not decode the JSON from the file '{config_file}'.")
            return None
