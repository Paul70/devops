from .devops_importer import impoert_derived_instance

class CliCommand:
    def __init__(self):
        self.devops_instance = impoert_derived_instance() 
        pass

    def cli_bootstrap(self):
        self.devops_instance.bootstrap()
        pass

    def cli_prepare(self):
        self.devops_instance.prepare() 
        pass

    def cli_build(self):
        self.devops_instance.build()
        pass