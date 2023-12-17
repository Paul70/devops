#! /usr/bin/python3
import json
from pathlib import Path
import os.path

class Utility:

    def loadProfile(project, profile = ""):
        if not profile:
            profile = "/home/paul/.config/devops/default-config.json"
        elif os.path.isfile(profile):
            # specified profile is in the project root dir
            pass
        elif os.path.isfile("/home/paul/.config/devops/"+profile):
            profile = "/home/paul/.config/devops/"+profile
        else:
            print("Profile " + profile + " not found")
        with open(profile) as file:
            profile_dict = json.load(file)
        file.close()
        print("devops.py (" + project + "): Using config: "+ profile)
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