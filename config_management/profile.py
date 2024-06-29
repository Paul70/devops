#! /usr/bin/python3
import json

from .devops_file import DevopsFile

def create_devops_profile(recipe):

    isinstance(recipe, DevopsFile)

    # parameter array structure:
    # [0]: name
    # [1]: profile description
    # [2]: operating system: name [0], version [1] 
    # [3]: ide: name [0], settings display name [1]
    # [4]: compiler: name [0], version [1], major [2], minor [3], path [4]
    # [5]: build: directory [0], type [1], jobs [2]

    name = parameter_array[0]
    display_name = parameter_array[3]["name"]
    description = parameter_array[1]
    os = parameter_array[2]["name"] + " " + parameter_array[2]["version"]
    compiler_path = parameter_array[4]["path"]
    compiler_version_major = parameter_array[4]["major"]
    build_type = parameter_array[5]["type"] 
    build_jobs = parameter_array[5]["jobs"]

    profile = {
        "label": name,
        "os": os,
        "cmakeUserPresets": {
            "configurePresets": [
                {
                    "name": display_name,
                    "displayName": display_name,
                    "description": description,
                    "cmakeExecutable": "conan",
                    "inherits": "conan-debug",
                    "cacheVariables": {
                        "CMAKE_CXX_COMPILER": compiler_path + "g++",
                        "CMAKE_CXX_COMPILER_AR": compiler_path + "gcc-ar",
                        "CMAKE_CXX_COMPILER_RANLIB": compiler_path + "gcc-ranlib",
                        "CMAKE_C_COMPILER": compiler_path + "gcc",
                        "CMAKE_C_COMPILER_AR": compiler_path + "gcc-ar",
                        "CMAKE_C_COMPILER_RANLIB": compiler_path + "gcc-ranlib" 
                    }
                }
            ],
            "buildPresets": [
                {
                    "name": display_name,
                    "configurePreset": display_name,
                    "jobs": build_jobs
                }
            ]
        },
        "conanProfile": {
            "name": name,
            "include": "default",
            "settings": {
                "build_type": build_type,
                "compiler.version": compiler_version_major
            },
            "conf": {
                "tools.build:jobs": build_jobs,
                "tools.build:compiler_executables": f"{{'c': '{compiler_path}gcc', 'cpp': '{compiler_path}g++'}}"
            }
        }
    }

    with open(f"{parameter_array[0]}.json", 'w') as json_file:
        json.dump(profile, json_file, indent=4)
    pass

def change_build_type():
    pass




def main():
    name = "slabstock-profile"
    decription = "Slabstock project settings and configuration."
    os = {
        "name": "Ubuntu",
        "version": "22.04.4 LTS",
    }
    ide = {
        "name": "qtcreator",
        "settings_display_name": "GCC-13.1.0-Debug" 
    }
    compiler = {
        "name": "gcc",
        "version": "13.1.0",
        "major": 13,
        "minor": 1,
        "path": "/opt/gcc-13.1.0-build/bin/"
    }
    build = {
        "directory": "./build",
        "type": "debug",
        "jobs": 16
    }
    create_devops_profile([name, decription, os, ide, compiler, build])
    pass


if __name__ == '__main__':
    main()
