import importlib.util
import inspect
import os


def impoert_derived_instance():
    devops_file = "/devopsfile.py"
    devops_file_name = "devopsfile"
    devops_file_path = os.getcwd() + devops_file
    devops_base_class_name = "DevopsFile"

    try:
        # Load the module from file
        spec = importlib.util.spec_from_file_location(devops_file_name, devops_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        print("hier")

        # Get the base class reference
        base_class = getattr(module, devops_base_class_name)
        
        # Find the derived class
        devops_derived_class = None
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, base_class) and obj is not base_class:
                devops_derived_class = obj
                break
        
        if devops_derived_class:
            # Instantiate the derived class
            #instance = derived_class("Alice")
            print("sdfadg")
            instance = devops_derived_class()
            #print(f"Class '{devops_derived_class.__name__}' instantiated with name: {instance.name}")
            print(f"Class '{devops_derived_class.__name__}' instantiated with name:")
            print(instance.function_of_Slabtock())  # This should call the `greet` method if it's DerivedClass

            # Return the derived devops object
            return instance

        else:
            print(f"No class derived from {devops_base_class_name} found in the module.")
            return None

    except FileNotFoundError:
        print(f"Project devops file '{devops_file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading or executing the module: {e}")
        return None


