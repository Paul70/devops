import os
import sys

from .utility import load_json_file_to_dict, validate_and_handle_dict


"""
    Hint: Top level porject path using this devops as managment tool is
    given via 
"""


class UserPresets:
    file_name = "/DevopsUserPresets.json"
    presets_dict = None
    allowed_key_set = [
        'settings_build',
        'settings_compiler',
        'settings_ide'
    ] 

    def __init__(self):
        self.presets_dict = load_json_file_to_dict(os.getcwd() + self.file_name)
        validate_and_handle_dict(self.presets_dict, self.allowed_key_set)
        
    
    def get_ide_settings(self):
        try:
            return self.presets_dict["settings_ide"]
        except KeyError as e:
            sys.exit(f"{os.getcwd() + self.file_name}: {e}")
        
    def get_compiler_settings(self):
        try:
            return self.presets_dict["settings_compiler"]
        except KeyError as e:
            sys.exit(f"{os.getcwd() + self.file_name}: {e}")

    def get_build_settings(self):
        try:
            return self.presets_dict["settings_build"]
        except KeyError as e:
            sys.exit(f"{os.getcwd() + self.file_name}: {e}")