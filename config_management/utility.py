#! /usr/bin/python3
import json
import os.path
import platform
import sys
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

def remove_file(file_path):
    """
    Remove a file at the specified path.

    Args:
        file_path (str): The path to the file to be deleted.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the program does not have permission to delete the file.
        Exception: If any other error occurs during file deletion.
    """

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

def load_json_file(file_path):
    """
    Load a JSON file and handle exceptions.
    
    Parameters:
    file_path (str): The path to the JSON file.
    
    Returns:
    dict: The loaded JSON data if successful, otherwise None.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        print(f"JSON file {file_path} loaded successfully.")
        return data
    except FileNotFoundError:
        sys.exit(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        sys.exit(f"Error: The file '{file_path}' is not a valid JSON file.")
    except Exception as e:
        sys.exit(f"An unexpected error occurred: {e}")
    return None

###################################################################################################

def write_dict_to_json(data, filename):
    """
    Write a Python dictionary to a JSON file with error handling.
    Methods creates non existing folders.
    
    Parameters:
    data (dict): The dictionary to be written to JSON.
    filename (str): The filename/path to write the JSON data.
    
    Returns:
    bool: True if successfully wrote the JSON data, False otherwise.
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Successfully wrote JSON data to '{filename}'")
        return True
    except IOError as e:
        sys.exit(f"Error: Could not write to file '{filename}': {e}")
    except Exception as e:
        sys.exit(f"Error: Unexpected error occurred: {e}")


