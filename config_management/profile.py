#! /usr/bin/python3
import json
import os

from .user_presets import UserPresets
from .utility import load_json_file_to_dict, detect_os_info

# create the devops profile needed to create the conan profile

class DevopsProfile:
    user_presets = None
    profile_dict = None

    def __init__(self):
        self.user_presets = UserPresets() 

    def is_empty(self):
        if self.user_presets.empty == True:
            return True
        else:
            return False


    def create_devops_profile(self, cmake_bin_path = None):
        current_script_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_script_path)
        parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
        profile_template = parent_directory + "/resources/profile_template.json"
        
        self.profile_dict = load_json_file_to_dict(profile_template)
        print(self.user_presets.get_build_settings())

        settings_compiler = self.user_presets.get_compiler_settings()
        settings_build = self.user_presets.get_build_settings()
        settings_ide = self.user_presets.get_ide_settings()
        settings_conan = self.user_presets.get_conan_settings()
        settings_compiler_path = settings_compiler["path"]

        label = "devops-user-settings-profile"

        # basic information section
        self.profile_dict["label"] = label
        self.profile_dict["os"] = detect_os_info()["os_name"]

        # cmake user presets section - configure presets
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["name"] = settings_ide["name"]
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["displayName"] = settings_ide["settings_display_name"]
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["description"] = "User and platform specific project settings and configuration."
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cmakeExecutable"] = cmake_bin_path
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["inherits"] = "conan-debug" # fixed value

        # cmake cache variables
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_CXX_COMPILER"] = settings_compiler_path + "g++"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_CXX_COMPILER_AR"] = settings_compiler_path + "gcc-ar"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_CXX_COMPILER_RANLIB"] = settings_compiler_path + "gcc-ranlib"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_C_COMPILER"] = settings_compiler_path + "gcc"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_C_COMPILER_AR"] = settings_compiler_path + "gcc-ar"
        self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_C_COMPILER_RANLIB"] = settings_compiler_path + "gcc-ranlib"

        # cmake user presets section - build presets
        self.profile_dict["cmakeUserPresets"]["buildPresets"][0]["name"] = settings_ide["name"]
        self.profile_dict["cmakeUserPresets"]["buildPresets"][0]["configurePreset"] = settings_ide["name"]
        self.profile_dict["cmakeUserPresets"]["buildPresets"][0]["jobs"] = settings_build["parallel_builds"]

        # conan profile section
        self.profile_dict["conanProfile"]["name"] = settings_conan["name"]
        self.profile_dict["conanProfile"]["include"] = settings_conan["include_profile"]
        self.profile_dict["conanProfile"]["settings"]["build_type"] = settings_build["build_type"]
        self.profile_dict["conanProfile"]["settings"]["compiler"] = settings_compiler["name"]
        self.profile_dict["conanProfile"]["settings"]["compiler.cppstd"] = settings_compiler["cppstd"]
        self.profile_dict["conanProfile"]["settings"]["compiler.libcxx"] = settings_compiler["libcxx"]
        self.profile_dict["conanProfile"]["settings"]["compiler.version"] = settings_compiler["major"]
        self.profile_dict["conanProfile"]["conf"]["tools.build:jobs"] = settings_build["parallel_builds"]
        self.profile_dict["conanProfile"]["conf"]["tools.build:compiler_executables"] = f"{{'c': '{settings_compiler_path}gcc', 'cpp': '{settings_compiler_path}g++'}}"

        # write the profile file.
        with open(f"devopsprofile.json", 'w') as json_file:
            json.dump(self.profile_dict, json_file, indent=4)
        pass


    def get_conan_profile_name(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.profile_dict = load_json_file_to_dict(file)
        return self.profile_dict["conanProfile"]["name"]
    
    
    def get_conan_profile_include(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.profile_dict = load_json_file_to_dict(file)
        return self.profile_dict["conanProfile"]["include"]


    def get_conan_profile_settings(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.profile_dict = load_json_file_to_dict(file)
        return self.profile_dict["conanProfile"]["settings"]


    def get_conan_profile_conf(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.profile_dict = load_json_file_to_dict(file)
        return self.profile_dict["conanProfile"]["conf"]


    def get_cmake(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.profile_dict = load_json_file_to_dict(file)
        return self.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cmakeExecutable"]    


    def get_cmake_user_presets(self):
        file = os.getcwd() + "/devopsprofile.json"
        self.profile_dict = load_json_file_to_dict(file)
        return self.profile_dict["cmakeUserPresets"]

