from .user_presets import UserPresets
from .conan_importer import ConanImporter

class DevopsFile():
    """
    The base class for all user project configuration recipes
    """
    def __init__(self):
        self.devopsUserPresets = UserPresets()
        self.conanImport = ConanImporter() # hier liegt der Hase im Pfeffer
        pass

    
    def bootstrap(self, args):
        print("This is the base class bootstrap method.")
        #print("Conan name:", self.conanImport.import_name_from_conan())
        pass
    


