import os
import json
from PIL import Image
import customtkinter
from customtkinter import CTkImage
from utils import load_json_config

class GameConfigManager:
    LAST_CONFIG_PATH = 'last_game_config.json'

    @staticmethod
    def load_game_icon(config_path=None):
        if config_path and os.path.exists(config_path):
            config = load_json_config(config_path)
            game_icon_path = 'gameIcons/' + config.get('game_icon', 'No_image_available.svg.png')
        else:
            game_icon_path = 'gameIcons/No_image_available.svg.png'
        
        return CTkImage(light_image=Image.open(game_icon_path), size=(250, 250))

    @staticmethod
    def save_last_game_config(config_path):
        with open(GameConfigManager.LAST_CONFIG_PATH, 'w') as file:
            json.dump({'last_config': config_path}, file)

    @staticmethod
    def load_last_game_config():
        if os.path.exists(GameConfigManager.LAST_CONFIG_PATH):
            with open(GameConfigManager.LAST_CONFIG_PATH, 'r') as file:
                data = json.load(file)
                return data.get('last_config')
        return None