#! /usr/bin/python3

import json
from pathlib import Path

class Utility:

    def export(self, data, folder, label):
        Path(folder).mkdir(parents=True, exist_ok=True)
        file = open(folder+label, "w")
        if "json" in label:
            file.write(json.dumps(data, indent=4))
        else:
            file.writelines(data)
        file.close()
        return file