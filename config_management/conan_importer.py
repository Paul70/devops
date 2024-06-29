import os
from conans.client.loader import ConanFileLoader

class ConanImporter:
    conanfile = "/conanfile.py"
    conanData = None

    def __init__(self):
        try:
            # Path to your conanfile.py
            file_path = os.getcwd() + self.conanfile
            print(file_path)

            # Create a loader object
            loader = ConanFileLoader(None, None)

            # Load the conanfile
            self.conanData = loader.load_conanfile(file_path, None)

        except FileNotFoundError:
            return 
        pass

    def import_name_from_conan(self):
        return self.conanData.name
    
    # def import_author_from_conan(self):
    #     return self.conanData.author
    
    # def import_version_from_conan(self):
    #     return self.conanData.version
