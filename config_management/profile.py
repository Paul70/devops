#! /usr/bin/python3
import json
import os

from .user_presets import UserPresets
from .utility import detect_os_info

# create the devops profile needed to create the conan profile

class DevopsProfile:
    user_presets_dict = None
    profile_dict = None

    def __init__(self):
        self.user_presets_dict = UserPresets() 
        

    def __load_profile__(self,input_file):
        try:
            with open(input_file, 'r') as file:
                 self.profile_dict = json.load(file)

        except FileNotFoundError as e:
            print(e)
            return 
        except Exception as e:
            print(e)
            return 
        pass
        

    def print_banner(self):
        pass

    def create_devops_profile(self):
        current_script_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_script_path)
        parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
        profile_template = parent_directory + "/resources/profile_template.json"
        
        self.__load_profile__(profile_template)

        compiler_settings = self.user_presets_dict.get_compiler_settings()
        compiler_path = compiler_settings["path"]

        build_settings = self.user_presets_dict.get_build_settings()
        ide_settings = self.user_presets_dict.get_ide_settings()

        label = "devops-user-settings-profile"

        # basic information section
        self.profile_dict["label"] = label
        self.profile_dict["os"] = detect_os_info()["os_name"]

        # cmake user presets section - configure presets
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["name"] = ide_settings["name"]
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["displayName"] = ide_settings["settings_display_name"]
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["description"] = "User and platform specific project settings and configuration."
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cmakeExecutable"] = "conan"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["inherits"] = "conan-debug"

        # cmake cache variables
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_CXX_COMPILER"] = compiler_path + "g++"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_CXX_COMPILER_AR"] = compiler_path + "gcc-ar"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_CXX_COMPILER_RANLIB"] = compiler_path + "gcc-ranlib"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_C_COMPILER"] = compiler_path + "gcc"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_C_COMPILER_AR"] = compiler_path + "gcc-ar"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_C_COMPILER_RANLIB"] = compiler_path + "gcc-ranlib"

        # cmake user presets section - build presets
        self.profile_dict["cmakeUserPresets"]["buildPresets"][0]["name"] = ide_settings["name"]
        self.profile_dict["cmakeUserPresets"]["buildPresets"][0]["configurePreset"] = ide_settings["name"]
        self.profile_dict["cmakeUserPresets"]["buildPresets"][0]["parallel_builds"] = build_settings["parallel_builds"]

        # conan profile section
        self.profile_dict["conanProfile"]["name"] = "devops_conan_profile"
        self.profile_dict["conanProfile"]["include"] = "default"
        self.profile_dict["conanProfile"]["settings"]["build_type"] = build_settings["target"]
        self.profile_dict["conanProfile"]["settings"]["compiler.version"] = compiler_settings["major"]
        self.profile_dict["conanProfile"]["conf"]["tools.build:jobs"] = build_settings["parallel_builds"]
        self.profile_dict["conanProfile"]["conf"]["tools.build:compiler_executables"] = f"{{'c': '{compiler_path}gcc', 'cpp': '{compiler_path}g++'}}"

        with open(f"devopsprofile.json", 'w') as json_file:
            json.dump(self.profile_dict, json_file, indent=4)
        pass

    def get_conan_profile_name(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.__load_profile__(file)
        return self.profile_dict["conanProfile"]["name"]
    
    def get_conan_profile_include(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.__load_profile__(file)
        return self.profile_dict["conanProfile"]["include"]

    def get_conan_profile_settings(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.__load_profile__(file)
        return self.profile_dict["conanProfile"]["settings"]
    
    def get_conan_profile_conf(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.__load_profile__(file)
        return self.profile_dict["conanProfile"]["conf"]
    
    def get_cmkae(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.__load_profile__(file)
        return self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cmakeExecutable"]



    # hier kann ich jetzt alle getter schreiben, die ich brauch        
        
        

