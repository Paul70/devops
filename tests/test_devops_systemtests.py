import json
import os 
import unittest

from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from devops.config_management.devops_file import DevopsFile
from config_management.utility import load_json_file_to_str

# global root path vairable
PROJECT_ROOT = Path(
    __file__).parent.absolute() # absolute is required, because debian and ubuntu defaults are different

class SystemTestDevopsFile(DevopsFile):
    project_root = str(PROJECT_ROOT)

    def bootstrap(self):
        pass
    

    def prepare(self):
        pass



class TestDevopsSystemTest(unittest.TestCase):

    def setUp(self):
        self.mock_json_data_user_presets_var1 = {
            "settings_ide": {
                "name": "GCC-13.1.0-Debug-qtcreator",
                "settings_display_name": "GCC-13.1.0-Debug", 
                "theme": "dark",
                "font_size": 9
            },
            "settings_compiler":  {
                "name": "gcc",
                "version": "13.1.0",
                "major": 13,
                "minor": 1,
                "cppstd": "gnu17",
                "libcxx": "libstdc++11",
                "path": "/opt/gcc-13.1.0-build/bin/"
            },
            "settings_build": {
                "directory": "./build",
                "build_type": "Debug",
                "parallel_builds": 16
            },
            "settings_conan": {
                "name": "devops_conan_profile",
                "include_profile": "default"
            }
        }
        self.json_string_user_presets_var1 = json.dumps(self.mock_json_data_user_presets_var1)
        self.devops_profile_template_read_data = load_json_file_to_str(os.getcwd() + "/devops/tests/test_data/profile_template.json")


    def test_bootstrap_command_no_user_presets(self):

        with patch("builtins.open", side_effect = FileNotFoundError):
            system_test = SystemTestDevopsFile()
            self.assertTrue(system_test.__devops_profile__.is_empty())
            self.assertFalse(system_test.__has_devops_profile__)
            system_test.bootstrap()
        pass

    def test_prepare_command_no_user_presets(self):
        with patch("builtins.open", side_effect = FileNotFoundError):
            system_test = SystemTestDevopsFile()
            self.assertTrue(system_test.__devops_profile__.is_empty())
            self.assertFalse(system_test.__has_devops_profile__)
            system_test.prepare()    
        pass

    
    def test_bootstrap_command_with_user_presets(self):

        mock_user_presets_read_data = mock_open(read_data=self.json_string_user_presets_var1).return_value                # 1. builtin open call loading the user presets json file 
        mock_devops_profile_template_read_data = mock_open(read_data=self.devops_profile_template_read_data).return_value # 2. builtin open call loading the devops profile template
        mock_devops_profile_jsonDump_read_data = mock_open().return_value                                                 # 3. builtin open call for writing the new devops profile

        with patch("builtins.open", side_effect = [mock_user_presets_read_data, 
                                                   mock_devops_profile_template_read_data,
                                                   mock_devops_profile_jsonDump_read_data]):
            system_test = SystemTestDevopsFile()
            self.assertFalse(system_test.__devops_profile__.is_empty())
            self.assertTrue(system_test.__has_devops_profile__)
            system_test.bootstrap()

            ## next thing to test is to give a good error message if there is a key error in
            ## the user presets.
        pass


if __name__ == '__main__':
    unittest.main()