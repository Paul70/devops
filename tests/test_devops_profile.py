import os 
import unittest
from unittest.mock import patch, MagicMock, mock_open

from config_management.profile import DevopsProfile
from config_management.utility import load_json_file_to_str



class TestDevopsProfile(unittest.TestCase):
    #config_management.user_presets.open
    @patch('config_management.user_presets.UserPresets')
    @patch('config_management.utility.detect_os_info')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"settings_ide": { "name": "VSCode", "settings_display_name": "Visual Studio Code" }, "settings_compiler":  { "major": 9, "path": "/usr/bin/" }, "settings_build": { "target": "x86_64", "parallel_builds": 4} }')
    def test_init_loads_profile_dict(self, mock_open, mock_detect_os_info, MockUserPresets):

        """Test that
            - creation of a DevopsProfile instance works, wich includes the creation of
              a UserPresets object instance.
            - all class attributes are initialized correctly.
        """

        # Setup
        mock_detect_os_info.return_value = {"os_name": "Linux"}
        mock_user_presets = MockUserPresets.return_value
        mock_user_presets.get_compiler_settings.return_value = {"path": "/usr/bin/", 
                                                                "major": 9}
        mock_user_presets.get_build_settings.return_value = {"parallel_builds": 4, 
                                                             "target": "x86_64"}
        mock_user_presets.get_ide_settings.return_value = {"name": "VSCode", 
                                                           "settings_display_name": "Visual Studio Code"}

        # Instantiate the DevopsProfile class and create
        devops_profile = DevopsProfile()

        # Assertions for initialization
        self.assertIsNotNone(devops_profile.user_presets.get_compiler_settings())
        compiler_settings_dict = devops_profile.user_presets.get_compiler_settings()
        self.assertEqual(compiler_settings_dict["path"], "/usr/bin/")
        self.assertEqual(compiler_settings_dict["major"], 9)

        self.assertIsNotNone(devops_profile.user_presets.get_build_settings())
        build_settings_dict = devops_profile.user_presets.get_build_settings()
        self.assertEqual(build_settings_dict["parallel_builds"], 4)
        self.assertEqual(build_settings_dict["target"], "x86_64")

        self.assertIsNotNone(devops_profile.user_presets.get_ide_settings())
        build_ide_dict = devops_profile.user_presets.get_ide_settings()
        self.assertEqual(build_ide_dict["name"], "VSCode")
        self.assertEqual(build_ide_dict["settings_display_name"], "Visual Studio Code")

        self.assertIsNotNone(devops_profile.user_presets)

        # Attributes
        self.assertIsNotNone(devops_profile.user_presets)

        # at this point, devops_profile.profile_dict has to be none since 
        # create_devops_profile() has not been called yet.
        self.assertIsNone(devops_profile.profile_dict)
        pass


    @patch('config_management.user_presets.UserPresets')
    @patch('config_management.utility.detect_os_info')
    @patch('json.dump')
    def test_create_devops_profile(self, mock_json_dump, mock_detect_os_info, MockUserPresets):

        """Test that
            - creation of a DevopsProfile instance works, wich includes the creation of
              a UserPresets object instance.
            - all class attributes are initialized correctly.
        """

        # Mocked file content loaded during this test via built-in open() method
        # Note, using the patch decorator as in the first test of this suite is somehow more 
        # difficult since the built-in open function is called twice, in 
        # - devops_profile = DevopsProfile()
        # - devops_profile.create_devops_profile()
        # To achieve that mock_open() has different read_data content, we need to define side_effect
        # and this is difficult using a patch decorator

        # Setup
        mock_detect_os_info.return_value = {"os_name": "Linux"}
        mock_user_presets = MockUserPresets.return_value
        mock_user_presets.get_compiler_settings.return_value = {"path": "/usr/bin/", "major": "9"}
        mock_user_presets.get_build_settings.return_value = {"parallel_builds": 4, "target": "x86_64"}
        mock_user_presets.get_ide_settings.return_value = {"name": "VSCode", "settings_display_name": "Visual Studio Code"}

        user_presets_read_data = \
            '{ \
                "settings_ide": { \
                    "name": "VSCode", \
                    "settings_display_name": "Visual Studio Code" \
                }, \
                "settings_compiler": { \
                    "name": "MSVC", \
                    "cppstd" : "gnu17", \
                    "libcxx": "libstdc++11", \
                    "major": 9, \
                    "path": "/usr/bin/" \
                }, \
                "settings_build": { \
                    "build_type": "Debug", \
                    "target": "x86_64", \
                    "parallel_builds": 4 \
                } \
            }'
        devops_profile_template_read_data = load_json_file_to_str(os.getcwd() + "/devops/tests/test_data/profile_template.json")
        devops_profile_jsonDump_read_data = ""

        mock_user_presets_read_data = mock_open(read_data=user_presets_read_data).return_value                       # 1. builtin open call
        mock_devops_profile_template_read_data = mock_open(read_data=devops_profile_template_read_data).return_value # 2. builtin open call
        mock_devops_profile_jsonDump_read_data = mock_open().return_value # 3. builtin open call

        # Instantiate the DevopsProfile class
        with patch("builtins.open", side_effect = [mock_user_presets_read_data, 
                                                   mock_devops_profile_template_read_data,
                                                   mock_devops_profile_jsonDump_read_data]):
            devops_profile = DevopsProfile()

            # Call create_devops_profile method
            self.assertIsNotNone(devops_profile.user_presets.get_compiler_settings())
            devops_profile.create_devops_profile()

             # Check that json.dump was called with the correct arguments
            mock_json_dump.assert_called_once_with(devops_profile.profile_dict, mock_devops_profile_jsonDump_read_data, indent=4)

            # Check if the profile_dict is updated correctly
            self.assertEqual(devops_profile.profile_dict["label"], "devops-user-settings-profile")
            self.assertEqual(devops_profile.profile_dict["os"], "Linux")
            self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["configurePresets"][0]["name"], "VSCode")
            self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["configurePresets"][0]["displayName"], "Visual Studio Code")
            self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cmakeExecutable"], None)
            self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["configurePresets"][0]["inherits"], "conan-debug")
            self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["configurePresets"][0]["cacheVariables"]["CMAKE_CXX_COMPILER"], "/usr/bin/g++")
            self.assertEqual(devops_profile.profile_dict["cmakeUserPresets"]["buildPresets"][0]["jobs"], 4)
            self.assertEqual(devops_profile.profile_dict["conanProfile"]["name"], "devops_conan_profile")
            self.assertEqual(devops_profile.profile_dict["conanProfile"]["settings"]["compiler.version"], 9)
            self.assertEqual(devops_profile.profile_dict["conanProfile"]["conf"]["tools.build:jobs"], 4)
            self.assertEqual(devops_profile.profile_dict["conanProfile"]["conf"]["tools.build:compiler_executables"], "{'c': '/usr/bin/gcc', 'cpp': '/usr/bin/g++'}")
            pass

if __name__ == '__main__':
    unittest.main()
