from .devops_importer import import_derived_instance

class CliCommand:
    def __init__(self):
        # After this line of code, we can use all attributes of 
        # the user devopsfile.py
        self.devops_instance = import_derived_instance() 
        pass

    def cli_bootstrap(self):
        print(self.devops_instance.project_root)
        self.devops_instance.bootstrap()
        pass

    def cli_prepare(self):
        self.devops_instance.prepare() 
        pass

    def cli_build(self):
        self.devops_instance.build()
        pass