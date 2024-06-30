import json
import os

from .utility import validate_and_handle_dict

class UserPresets:
    file_name = "/DevopsUserPresets.json"
    presets_dict = None
    allowed_key_set = [
        'settings_build',
        'settings_compiler',
        'settings_ide'
    ] 

    def __init__(self):
        try:
            # Specify the path to your JSON file
            path = os.getcwd() + self.file_name 

            with open(path, 'r') as file:
                 self.presets_dict = json.load(file)

        except FileNotFoundError as e:
            print(e)
            return 
        
        try:
            validate_and_handle_dict(self.presets_dict, self.allowed_key_set)
        except ValueError as e:
            print(e)
            return
        
    
    def get_ide_settings(self):
        try:
            return self.presets_dict["settings_ide"]
        except KeyError:
            return
        
    def get_compiler_settings(self):
        try:
            return self.presets_dict["settings_compiler"]
        except KeyError:
            return

    def get_build_settings(self):
        try:
            return self.presets_dict["settings_build"]
        except KeyError:
            return