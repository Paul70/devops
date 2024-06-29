import json
import os

class UserPresets:
    fileName = "/DevopsUserPresets.json"
    presetsData = None

    def __init__(self):
        try:
            # Specify the path to your JSON file
            path = os.getcwd() + self.fileName 

            with open(path, 'r') as file:
                 self.presetsData = json.load(file)

        except FileNotFoundError:
            return 
        pass

    def get_author(self):
        try:
            return self.presetsData["author"]
        except KeyError:
            return 

    def get_version(self):
        try:
            return self.presetsData["version"]
        except KeyError:
            return

    def get_name(self):
        try:
            return self.presetsData["name"]
        except KeyError:
            return
    
    def get_ide_settings(self):
        try:
            return self.presetsData["settings_ide"]
        except KeyError:
            return
        
    def get_compiler_settings(self):
        try:
            return self.presetsData["settings_compiler"]
        except KeyError:
            return

    def get_build_settings(self):
        try:
            return self.presetsData["settings_build"]
        except KeyError:
            return