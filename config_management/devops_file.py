import os
import json
import subprocess
import sys

from .user_presets import UserPresets
from .conan_importer import ConanImporter
from .profile import DevopsProfile
from .utility import remove_file, load_json_file, write_dict_to_json

class DevopsFile():
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

    def get_devops_profile(self, cmake_bin = None):
        profile = DevopsProfile()
        profile.create_devops_profile(cmake_bin)
        return profile

    def create_conan_profile(self):
        # hier noch das default conan profile machen
        devops_profile = self.get_devops_profile()

        # load devops profile
        home_directory_user = os.path.expanduser("~")
        file = home_directory_user + "/.conan2/profiles/" + devops_profile.get_conan_profile_name()

        conan_porfile = open(file, "w")
        conan_porfile.writelines("# This is an automatically generated file.\n \
                                  # Contents will be overwritten, do not edit manually.\n")

        # include section
        conan_porfile.writelines("include("+ devops_profile.get_conan_profile_include() +")\n")

        # settings section
        conan_porfile.writelines("\n[settings]\n")
        devops_conan_settings_dict = devops_profile.get_conan_profile_settings() 
        for key, value in devops_conan_settings_dict.items():
            conan_porfile.writelines(key+"="+str(value)+"\n")


        # conf section
        conan_porfile.writelines("\n[conf]\n")
        devops_conan_conf_dict = devops_profile.get_conan_profile_conf() 
        for key, value in devops_conan_conf_dict.items():
            conan_porfile.writelines(key+"="+str(value)+"\n")
        
        conan_porfile.close()
        self.conan_profile_path = file

        # Remove already existing CMakeUserPresets.json and CMakeLists.txt.user files since they
        # may cause trouble.
        remove_file(self.project_root + "./CMakeUserPresets.json")
        remove_file(self.project_root + "./CMakeLists.txt.user")
        pass


    def conan_install(self):
        result = subprocess.run(["conan install . -pr "+self.conan_profile_path+" -f json --build missing"], shell = True, capture_output = True, text = True)
        if result.stderr:
            print(result.stderr)
        if not result.stdout:
            print("devops.py: Error: Conan install, leaving project configuration process.")
            return
        
        self.build_dir = self.project_root + "/build/Debug/"
        self.conan_info_dir = self.build_dir + "conan_info/"

        # grep conan info graph
        conan_info_graph_dict = json.loads(result.stdout)
        write_dict_to_json(conan_info_graph_dict, self.conan_info_dir + "info_graph.json")
        pass

    def create_cmake_user_presets(self):
        cmake_bin = self.get_cmake_bin_from_conan_graph()
        devops_profile = self.get_devops_profile(cmake_bin)
        cmake_user_presets_devops = devops_profile.get_cmake_user_presets()

        print(self.project_root + "/CMakeUserPresets.json")

        cmake_user_presets_conan = load_json_file(self.project_root + "/CMakeUserPresets.json")
        print("hallo")
        cmake_user_presets_conan.update(cmake_user_presets_devops)
        print("hallo")
        write_dict_to_json(cmake_user_presets_conan, self.project_root + "/CMakeUserPresets.json")
        pass


        #conan_info_graph_dict["cmakeUserPresets"]["configurePresets"][0]["cmakeExecutable"] = cmakeBin
        #cmake_user_presets = open(file, "w")
        #cmake_user_presets.writelines(key+"="+str(value)+"\n")
        


    def get_cmake_bin_from_conan_graph(self):
        conan_info_graph_dict = load_json_file(self.conan_info_dir + "info_graph.json")
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
        




    
    
    def bootstrap(self, args):
        pass

    def prepare(self):
        pass

    def build(self):
        pass


    
    


