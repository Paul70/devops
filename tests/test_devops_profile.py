import unittest
from unittest.mock import patch, MagicMock
import json
import os

from config_management.profile import DevopsProfile, UserPresets, detect_os_info



class TestDevopsProfile(unittest.TestCase):
    
    @patch('config_management.user_presets.open', new_callable=unittest.mock.mock_open, read_data='{"settings_ide": {"name": "VSCode","settings_display_name": "Visual Studio Code"},"settings_compiler":  {"major": 9,"path": "/usr/bin/"},"settings_build": {"target": "x86_64","parallel_builds": 4}}')
    @patch('config_management.user_presets.UserPresets')
    @patch('config_management.utility.detect_os_info')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"cmakeUserPresets": {"configurePresets": {}, "buildPresets": {}}, "conanProfile": {"settings": {}, "conf": {}}}')
    def test_init_loads_profile_dict(self, mock_open, mock_detect_os_info, MockUserPresets, mock_user_presets_open):
        # Setup
        mock_detect_os_info.return_value = {"os_name": "Linux"}
        mock_user_presets = MockUserPresets.return_value
        mock_user_presets.get_compiler_settings.return_value = {"path": "/usr/bin/", "major": "9"}
        mock_user_presets.get_build_settings.return_value = {"parallel_builds": 4, "target": "x86_64"}
        mock_user_presets.get_ide_settings.return_value = {"name": "VSCode", "settings_display_name": "Visual Studio Code"}

        # Instantiate the DevopsProfile class
        devops_profile = DevopsProfile()

        #print("hallo")
        #print(devops_profile.user_presets_dict.get_compiler_settings())

        # Assertions for initialization
        self.assertIsNotNone(devops_profile.user_presets_dict.get_compiler_settings())
        self.assertIsNotNone(devops_profile.user_presets_dict)
        #self.assertIsNotNone(devops_profile.profile_dict)
        #self.assertIn("cmakeUserPresets", devops_profile.profile_dict)
        #self.assertIn("conanProfile", devops_profile.profile_dict)



    @patch('config_management.user_presets.open', new_callable=unittest.mock.mock_open, read_data='{"settings_ide": {"name": "VSCode","settings_display_name": "Visual Studio Code"},"settings_compiler":  {"major": 9,"path": "/usr/bin/"},"settings_build": {"target": "x86_64","parallel_builds": 4}}')
    @patch('config_management.user_presets.UserPresets')
    @patch('config_management.utility.detect_os_info')
    #@patch('config_management.profile.open', new_callable=mock_open)
    @patch('json.dump')
    #@patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=)
    def test_create_devops_profile(self, mock_json_dump, mock_open, mock_detect_os_info, MockUserPresets, mock_user_presets_open):
        # Setup
        mock_detect_os_info.return_value = {"os_name": "Linux"}
        mock_user_presets = MockUserPresets.return_value
        mock_user_presets.get_compiler_settings.return_value = {"path": "/usr/bin/", "major": "9"}
        mock_user_presets.get_build_settings.return_value = {"parallel_builds": 4, "target": "x86_64"}
        mock_user_presets.get_ide_settings.return_value = {"name": "VSCode", "settings_display_name": "Visual Studio Code"}

        # Instantiate the DevopsProfile class
        devops_profile = DevopsProfile()

        # Call create_devops_profile method
        self.assertIsNotNone(devops_profile.user_presets_dict.get_compiler_settings())

        devops_profile.create_devops_profile()

        # Check if the profile_dict is updated correctly
        self.assertEqual(devops_profile.profile_dict["label"], "devops-user-settings-profile")
        self.assertEqual(devops_profile.profile_dict["os"], "Linux")
        self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["configurePresets"][0]["name"], "VSCode")
        self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["configurePresets"][0]["displayName"], "Visual Studio Code")
        self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cmakeExecutable"], "conan")
        self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["configurePresets"][0]["inherits"], "conan-debug")
        self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_CXX_COMPILER"], "/usr/bin/g++")
        self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["buildPresets"][0]["parallel_builds"], 4)
        self.assertEqual(devops_profile.profile_dict["conanProfile"]["name"], "devops_conan_profile")
        self.assertEqual(devops_profile.profile_dict["conanProfile"]["settings"]["compiler.version"], 9)
        self.assertEqual(devops_profile.profile_dict["conanProfile"]["conf"]["tools.build:jobs"], 4)
        self.assertEqual(devops_profile.profile_dict["conanProfile"]["conf"]["tools.build:compiler_executables"], "{'c': '/usr/bin/gcc', 'cpp': '/usr/bin/g++'}")

        
        # Check if the JSON file is written correctly
        #mock_open().write.assert_called()
        mock_json_dump.assert_called_once_with(
            self.devops_profile.profile_dict, mock_open(), indent=4
        )

if __name__ == '__main__':
    unittest.main()
