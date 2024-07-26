import os
import json
import subprocess
import sys

from .user_presets import UserPresets
from .conan_importer import ConanImporter
from .profile import DevopsProfile
from .utility import remove_file, load_json_file_to_dict, write_dict_to_json

class DevopsFile():
    """
    Private class attributes
    """
    __devops_profile__ = None

    """
    The base class for all user project configuration recipes
    """
    project_root = None
    conan_profile_path = None
    build_dir = None
    conan_info_dir = None

    def __init__(self):
        self.devopsUserPresets = UserPresets()
        # need conan create or conan install command before
        #self.conanImport = ConanImporter() # hier liegt der Hase im Pfeffer
        pass



    def __set_devops_profile__(self, cmake_bin = None):
        self.__devops_profile__ = DevopsProfile()
        if self.__devops_profile__.is_empty():
            return False
        else:
            self.__devops_profile__.create_devops_profile(cmake_bin)
            return True
    


    def __create_default_conan_profile__(self):
        result = subprocess.run(["conan profile detect -f"], shell = True, capture_output = True, text = True)
        if result.stderr:
            print(result.stderr) # conan command output is written to stderr, just print the command output here
        if not result.stdout:
            sys.exit("devops.py: Error: Conan create default profile, leaving project configuration process.")
        home_directory_user = os.path.expanduser("~")
        return home_directory_user + "/.conan2/profiles/default"
    


    def __create_devops_conan_profile__(self):
        assert self.__devops_profile__ != None

        # load devops profile
        home_directory_user = os.path.expanduser("~")
        user_conan_profile = self.__devops_profile__.get_conan_profile_name()

        file = home_directory_user + "/.conan2/profiles/" + user_conan_profile

        conan_porfile = open(file, "w")
        conan_porfile.writelines("# This is an automatically generated file.\n \
                                  # Contents will be overwritten, do not edit manually.\n")

        # include section
        conan_porfile.writelines("include("+ self.__devops_profile__.get_conan_profile_include() +")\n")

        # writing custom conan profile section
        # if a devopsprofile setting field has no value, no conan entry will be written.

        # settings section
        conan_porfile.writelines("\n[settings]\n")
        devops_conan_settings_dict = self.__devops_profile__.get_conan_profile_settings() 
        for key, value in devops_conan_settings_dict.items():
            if value:
                conan_porfile.writelines(key+"="+str(value)+"\n")


        # conf section
        conan_porfile.writelines("\n[conf]\n")
        devops_conan_conf_dict = self.__devops_profile__.get_conan_profile_conf() 
        for key, value in devops_conan_conf_dict.items():
            if value:
                conan_porfile.writelines(key+"="+str(value)+"\n")
        
        conan_porfile.close()
        return file
    


    def create_conan_profile(self):
        if self.__set_devops_profile__():
            self.conan_profile_path = self.__create_devops_conan_profile__()
        else:
            self.conan_profile_path = self.__create_default_conan_profile__()

        # Remove already existing CMakeUserPresets.json and CMakeLists.txt.user files since they
        # may cause trouble.
        remove_file(self.project_root + "./CMakeUserPresets.json")
        remove_file(self.project_root + "./CMakeLists.txt.user")
        pass



    def conan_install(self):
        assert self.conan_profile_path != None

        result = subprocess.run(["conan install . -pr "+self.conan_profile_path+" -f json --build missing"], shell = True, capture_output = True, text = True)
        if result.stderr:
            print(result.stderr) # conan command output is written to stderr, just print the command output here
        if not result.stdout:
            print("devops.py: Error: Conan install, leaving project configuration process.")
            return
        
        self.build_dir = self.project_root + "/build/Debug/"
        self.conan_info_dir = self.build_dir + "conan_info/"

        # grep conan info graph, this is imprtant for extracting the cmake bin folder
        conan_info_graph_dict = json.loads(result.stdout)
        write_dict_to_json(conan_info_graph_dict, self.conan_info_dir + "info_graph.json")
        pass



    def create_cmake_user_presets(self):
        if self.__devops_profile__.is_empty():
            sys.exit("Cannot create a CMakeUserPresets.json with no DevopsUserPresets.json, leaving ...")

        cmake_bin = self.get_cmake_bin_from_conan_graph()
        self.__set_devops_profile__(cmake_bin)
        cmake_user_presets_devops = self.__devops_profile__.get_cmake_user_presets()

        print(self.project_root + "/CMakeUserPresets.json")

        cmake_user_presets_conan = load_json_file_to_dict(self.project_root + "/CMakeUserPresets.json")
        cmake_user_presets_conan.update(cmake_user_presets_devops)
        write_dict_to_json(cmake_user_presets_conan, self.project_root + "/CMakeUserPresets.json")
        pass
        


    def get_cmake_bin_from_conan_graph(self):
        conan_info_graph_dict = load_json_file_to_dict(self.conan_info_dir + "info_graph.json")
        cmake_bin_path = None
        
        try:
            for key in conan_info_graph_dict["graph"]["nodes"]:
                if "cmake/" in conan_info_graph_dict["graph"]["nodes"][key]["label"]:
                    cmake_bin_path = conan_info_graph_dict["graph"]["nodes"][key]["cpp_info"]["root"]["bindirs"][0] + "/cmake" 
                    break
        except KeyError as e:
            sys.exit(f"Conan info graph file is broken: {e}: re-run conan install")
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {e}")
        return cmake_bin_path 
        




    
    


