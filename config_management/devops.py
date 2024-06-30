#! /usr/bin/python3

import os
import subprocess
import json

from pathlib import Path
from utility import Utility

class DevOpsImpl:

    def __init__(self) -> None:
        self.conanProfile = ""
        self.buildType = ""
        self.buildDir = ""
        self.conanInfoDir = ""
        self.cmakeUserPresets = ""
        pass

    def checkProfile(self, project, configProfile = ""):
        print("\n======== checking project settings profile ========")
        print("devops.py (" + project + "): Calling update()")

        config_dict = Utility.loadProfile(project, configProfile)
        pass

    def update(self):
        print("\n======== updating project and dependencies ========")
        print("devops.py (PROJECT_NAME_VERSION): Calling update()")

    def build(self):
        pass


    # 
    # was ich hier noch einbauen muss oder besser ändern muss
    # fucntion create config, die aus einem conanprofile file ein cmake user presets erstellt
    # oder noch besser, ich erstelle aus einem ProjectUserConfig kit ein conan profile, speichere das
    # dann unter profiles ab und dann kann ich das direkt nutzen

    # (re-)writes conan profile
    # runs conan install command 

    def bootstrap(self, project = None, configProfile = None):
        print("\n======== Setting project configuration ========")
        Utility.printMethodInfo("devops.py", project, "Calling boostrap()")

        # dictionaries used within this method
        config_dict = {}
        conanGraph_dict = {}

        # load devops profile
        #config_dict = Utility.loadProfile(project, configProfile)


        if "conanProfile" in config_dict:
            self.conanProfile = self.createConanProfile(config_dict["conanProfile"])
        else:
            self.conanProfile = self.createConanProfile()  
            pass
        Utility.printMethodInfo("devops.py", project, "Conan profile generated: " + self.conanProfile)


        #file = Path("./CMakeLists.txt.user")
        #if file.is_file():
        #    Utility.printMethodInfo("devops.py", project, "Removing "+file.name+" since it may cause trouble.")
        #    subprocess.run(["rm "+file.name], shell = True, capture_output = False, text = False)        
        #file = Path("./CMakeUserPresets.json")
        #if file.is_file():
        #    Utility.printMethodInfo("devops.py", project, "Removing "+file.name+" since it may cause trouble.")
        #    subprocess.run(["rm "+file.name], shell = True, capture_output = False, text = False)
        #file = ""

        # first run conan install, write info graph to stdout 
        # and save stdout to file under build_dir/build_type/conan_info/...
        Utility.printMethodInfo("devops.py", project, "Running conan install command.")
        result = subprocess.run(["conan install . -pr "+self.conanProfile+" -f json --build missing"], shell = True, capture_output = True, text = True)
        if result.stderr:
            print(result.stderr)
        if not result.stdout:
            Utility.printMethodInfo("devops.py", project, "Error: Conan install, leaving project configuration process.")
            return
        

        # hier ist conan install schon gelaufen, kann dann auch das conanfile importieren

        conanGraph_dict = json.loads(result.stdout)
        self.buildType = conanGraph_dict["graph"]["nodes"]["0"]["settings"]["build_type"]
        self.buildDir  = conanGraph_dict["graph"]["nodes"]["0"]["build_folder"]
        self.conanInfoDir = self.buildDir + "/conan_info/"

    
        file = Utility.export(conanGraph_dict, self.conanInfoDir, "info_graph.json")
        Utility.printMethodInfo("devops.py", project, "Generated conan info graph: "+ file.name)
        file = ""

        # das hier ist das einzig wichtige
        result = subprocess.run(["conan graph info -f html ."], shell = True, capture_output = True, text = True)
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            file = Utility.export(result.stdout, self.conanInfoDir, "dependency_graph.html")
            Utility.printMethodInfo("devops.py", project, "Generated conan info graph html: "+ file.name)
        file = ""
        

        # check if we need cmake and its generator from conan cache
        # hier einfach checken ob es conan ist oder nicht

        for i_configPresets in config_dict["cmakeUserPresets"]["configurePresets"]:
            if not "cmakeExecutable" in i_configPresets:
               Utility.printMethodInfo("devops.py", project, "Warning: No cmake executable set in "+ configProfile+".") 
            elif i_configPresets["cmakeExecutable"] == "conan" or\
               i_configPresets["cmakeExecutable"] == "":
                Utility.printMethodInfo("devops.py", project, "Using conan cache cmake.") 

                # find cmake binary das hier ist relevant
                for key in conanGraph_dict["graph"]["nodes"]:
                    if "cmake/" in conanGraph_dict["graph"]["nodes"][key]["label"]:
                        cmakeBin = conanGraph_dict["graph"]["nodes"][key]["cpp_info"]["root"]["bindirs"][0] + "/cmake"
                        config_dict["cmakeUserPresets"]["configurePresets"][0]["cmakeExecutable"] = cmakeBin
                        Utility.printMethodInfo("devops.py", project, "Found "+ cmakeBin) 
                        break
                
                if not cmakeBin:
                    Utility.printMethodInfo("devops.py", project, "Warning: No cmake executable found.")
            else:
                continue

        # load CMakeUserPresets.json generated durting conan install()
        # we need this one to include conan toolchain file.
        with open("./CMakeUserPresets.json") as file:
            presets_conan = json.load(file)
        file.close()
        presets_conan.update(config_dict["cmakeUserPresets"])

        # export new CMakeUserPresets.json
        Utility.export(presets_conan, os.getcwd()+"/", "CMakeUserPresets.json")
        pass


    # Get a conan profile based on the default conan profile and the settings in
    # specified ProjectUserConig.json file which is located under: 
    #   ~/.config/devops/
    #
    # conanprofile will be located under:
    #   ~/.conan2/profiles/
    #
    # If no default conanprofile already exists, one will be generated with conan profile command.
    #
    # input: values: dictionary of conanprofile settings
    # output: of path created conanprofile
    # 
    def createConanProfile(self, values = {}):
        
        if not "include" in values or values["include"] == "":
            print("No include conanprofile set, using the system default one:\n")
            file = Path("/home/paul/.conan2/profiles/default")
            if not file.is_file():
                result = subprocess.run(["conan profile detect --force"], shell = True, capture_output = True, text = True)
                if result.stderr:
                    print(result.stderr)
                    return False
                values["include"] = file
                

        # create conanprofile file
        file = "/home/paul/.conan2/profiles/" + values["name"]
        conanporfile = open(file, "w")

        # write include section
        include = "include("+values["include"]+")\n"
        conanporfile.writelines(include+"\n")

        # write settings section
        if "settings" in values:
            settings = "[settings]\n"
            for key in values["settings"]:
                settings += key+"="+str(values["settings"][key])+"\n"
            conanporfile.writelines(settings+"\n")
        
        # write conf section
        if "conf" in values:
            config = "[conf]\n"
            for key in values["conf"]:
                config += key+"="+str(values["conf"][key])+"\n"
            conanporfile.writelines(config+"\n")

        conanporfile.close()
        return file
    







