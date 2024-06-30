import os

from .user_presets import UserPresets
from .conan_importer import ConanImporter
from .profile import DevopsProfile
from .utility import remove_file

class DevopsFile():
    """
    The base class for all user project configuration recipes
    """
    def __init__(self):
        self.devopsUserPresets = UserPresets()
        # need conan create or conan install command before
        #self.conanImport = ConanImporter() # hier liegt der Hase im Pfeffer
        pass

    def create_devops_profile(self):
        profile = DevopsProfile()
        profile.create_devops_profile()
        return profile

    def create_conan_profile(self):
        devops_profile = self.create_devops_profile()

        # load devops profile
        home_directory_user = os.path.expanduser("~")
        file = home_directory_user + "/.conan2/profiles/" + devops_profile.get_conan_profile_name()

        conan_porfile = open(file, "w")

        # write include section
        include = "include("+ devops_profile.get_conan_profile_include() +")\n"
        conan_porfile.writelines(include+"\n")

        # write settings section
        settings = "[settings]\n"
        devops_conan_settings_dict = devops_profile.get_conan_profile_settings() 
        print(devops_conan_settings_dict)
        for index, (key, value) in enumerate(devops_conan_settings_dict):
            print({key})
            print({value})
            #settings += key+"="+str(value)+"\n"
            #conan_porfile.writelines(settings+"\n")

        # write conf section
        conf = "[conf]\n"
        devops_conan_conf_dict = devops_profile.get_conan_profile_conf() 
        for key, value in devops_conan_conf_dict:
                conf += key+"="+str(value)+"\n"
                conan_porfile.writelines(settings+"\n")
        
        conan_porfile.close()

        # Remove already existing CMakeUserPresets.json and CMakeLists.txt.user files since they
        # may cause trouble.
        remove_file(os.getcwd() + "./CMakeUserPresets.json")
        remove_file(os.getcwd() + "./CMakeLists.txt.user")
        pass

    
    
    def bootstrap(self, args):
        print("This is the base class bootstrap method.")
        #print("Conan name:", self.conanImport.import_name_from_conan())
        pass

    def prepare(self):
        pass

    def build(self):
        pass


    
    


