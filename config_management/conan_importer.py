import os
from conans.client.loader import ConanFileLoader

class ConanImporter:
    conanfile = "/conanfile.py"
    conanData = None

    def __init__(self):
        try:
            # Path to your conanfile.py
            file_path = os.getcwd() + self.conanfile

            # Create a loader object
            loader = ConanFileLoader(None, None)

            # Load the conanfile
            self.conanData = loader.load_conanfile(file_path, None)

        except FileNotFoundError as e:
            print(e)
            return
        except Exception as e:
            print(e)
            return 

    def import_conan_name(self): 
        return self.conanData.name
    
    def import_conan_author(self):
         return self.conanData.author
    
    def import_conan_version(self):
         return self.conanData.version
