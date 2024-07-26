import os
import sys

from .utility import load_json_file_to_dict, validate_and_handle_dict


"""
    Hint: Top level porject path using this devops as managment tool is
    given via 
"""


class UserPresets:
    file_name = "/DevopsUserPresets.json"
    empty = False
    presets_dict = None
    allowed_key_set = [
        'settings_build',
        'settings_compiler',
        'settings_ide',
        'settings_conan'
    ] 

    def __init__(self):
        try:
            self.presets_dict = load_json_file_to_dict(os.getcwd() + self.file_name, False)
        except FileNotFoundError as e:
            print("No DevopsUserPresets.json found, continuing with conan settings ...")
            self.empty = True
            return
        except Exception as e:
            sys.exit(f"Error: Loading '{self.file_name}': {e}")

        validate_and_handle_dict(self.presets_dict, self.allowed_key_set)
        
    
    def get_ide_settings(self):
        try:
            return self.presets_dict["settings_ide"]
        except KeyError as e:
            return {}
        except Exception as e:
            sys.exit(f"{os.getcwd() + self.file_name}: {e}")
        
    def get_compiler_settings(self):
        try:
            return self.presets_dict["settings_compiler"]
        except KeyError as e:
            return {}
        except Exception as e:
            sys.exit(f"{os.getcwd() + self.file_name}: {e}")

    def get_build_settings(self):
        try:
            return self.presets_dict["settings_build"]
        except KeyError as e:
            return {}
        except Exception as e:
            sys.exit(f"{os.getcwd() + self.file_name}: {e}")
    
    def get_conan_settings(self):
        try:
            return self.presets_dict["settings_conan"]
        except KeyError as e:
            # in this case, we return a dictionary containing the information, that 
            # we need for setting up the conan profile.
            return {"name": "devops_conan_profile","include_profile": "default"} 
        except Exception as e:
            sys.exit(f"{os.getcwd() + self.file_name}: {e}")
