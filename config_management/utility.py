#! /usr/bin/python3
import json
import os.path
import platform
from pathlib import Path
from os.path import expanduser


"""
Validates that a dictionary only contains a defined set of keys.

:param input_dict: The dictionary to validate.
:param allowed_keys: A set of allowed keys.
:return: True if the dictionary only contains allowed keys, False otherwise.
"""
def validate_dict_key(input_dict, allowed_keys):
        return set(input_dict.keys()).issubset(allowed_keys)

###################################################################################################


"""
Validates that a dictionary only contains a defined set of keys.
In case of an allowed key, a "ValueError" exception is thrown.

:param input_dict: The dictionary to validate.
:param allowed_keys: A set of allowed keys.
:return: True if the dictionary only contains allowed keys, throw exception otherwise.
"""
def validate_and_handle_dict(input_dict, allowed_keys):
        if not validate_dict_key(input_dict, allowed_keys):
            raise ValueError(f"Invalid keys found. Allowed keys are: {allowed_keys}")

###################################################################################################


"""
    Detects the operating system name, version, and release.

    This function uses the platform module to retrieve information
    about the operating system on which the Python script is running.

    Returns:
        dict: A dictionary containing:
            - os_name (str): The name of the operating system (e.g., 'Windows', 'Darwin', 'Linux').
            - os_release (str): The release version of the operating system.
            - os_version (str): The version of the operating system.
"""
def detect_os_info():
    os_name = platform.system()

    # Get the operating system release and version
    os_release = platform.release()
    os_version = platform.version()

    # Return the information as a dictionary
    return {
        "os_name": os_name,
        "os_release": os_release,
        "os_version": os_version
    } 

###################################################################################################

"""
Remove a file at the specified path.

Args:
    file_path (str): The path to the file to be deleted.

Raises:
    FileNotFoundError: If the file does not exist.
    PermissionError: If the program does not have permission to delete the file.
    Exception: If any other error occurs during file deletion.
"""
def remove_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} has been deleted successfully.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except PermissionError:
        print(f"Permission denied: {file_path}.")
    except Exception as e:
        print(f"Error occurred while deleting file {file_path}: {e}")
    pass

###################################################################################################






class Utility:

    def loadProfile(project, profile = ""):
        if not profile:
            profile = expanduser("~") + "/.config/devops/default-debug-config.json"
        elif os.path.isfile(profile):
            # specified profile is in the project root dir
            pass
        elif os.path.isfile(expanduser("~") + "/.config/devops/" + profile):
            profile = expanduser("~") + "/.config/devops/" + profile
        else:
            Utility.printMethodInfo("utility.py", project, "Profile " + profile + " not found")
            return
        Utility.printMethodInfo("utility.py", project, "Reading profile " + profile)
        
        with open(profile) as file:
            profile_dict = json.load(file)
        file.close()
        return profile_dict


    def export(data, folder, label):
        Path(folder).mkdir(parents=True, exist_ok=True)
        file = open(folder+label, "w")
        if "json" in label:
            file.write(json.dumps(data, indent=4))
        else:
            file.writelines(data)
        file.close()
        return file
    
    def printMethodInfo(file = None, project = None, text = ""):
        print(file + " ("+project + "): " + text)
        pass 

    def printBannerInfo(text = ""):
        print("======== Devops-Recipe" + text + " ========")
        pass