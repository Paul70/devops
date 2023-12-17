#! /usr/bin/python3
import json
import os.path
from pathlib import Path
from os.path import expanduser

class Utility:

    def loadProfile(project, profile = ""):
        if not profile:
            profile = expanduser("~") + "/.config/devops/default-config.json"
        elif os.path.isfile(profile):
            # specified profile is in the project root dir
            pass
        elif os.path.isfile(expanduser("~") + "/.config/devops/" + profile):
            profile = expanduser("~") + "/.config/devops/" + profile
        else:
            Utility.printMethodInfo("utility.py", project, "Profile " + profile + "not found")
            return
        Utility.printMethodInfo("utility.py", project, "Reading profile " + profile)
        
        with open(profile) as file:
            profile_dict = json.load(file)
        file.close()
        return profile_dict


    def export(data, folder, label):
        Path(folder).mkdir(parents=True, exist_ok=True)
        file = open(folder+label, "w")
        if "json" in label:
            file.write(json.dumps(data, indent=4))
        else:
            file.writelines(data)
        file.close()
        return file
    
    def printMethodInfo(file = None, project = None, text = ""):
        print(file + " ("+project + "): " + text)
        pass 