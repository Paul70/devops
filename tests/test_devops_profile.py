import unittest
from unittest.mock import mock_open, patch
import json

# Assuming create_devops_profile is imported from the module where it is defined.
from devops.config_management.profile import create_devops_profile

class TestCreateDevopsProfile(unittest.TestCase):

    def setUp(self):
        self.parameter_array = [
            "devops_profile",
            "A profile description",
            {"name": "Ubuntu", "version": "20.04"},
            {"name": "VSCode", "settings_display_name": "Default"},
            {"name": "gcc", "version": "10", "major": "10", "minor": "2", "path": "/usr/bin/"},
            {"directory": "/build", "type": "Release", "jobs": 4}
        ]

        self.expected_profile = {
            "label": "devops_profile",
            "os": "Ubuntu 20.04",
            "cmakeUserPresets": {
                "configurePresets": [
                    {
                        "name": "VSCode",
                        "displayName": "VSCode",
                        "description": "A profile description",
                        "cmakeExecutable": "conan",
                        "inherits": "conan-debug",
                        "cacheVariables": {
                            "CMAKE_CXX_COMPILER": "/usr/bin/g++",
                            "CMAKE_CXX_COMPILER_AR": "/usr/bin/gcc-ar",
                            "CMAKE_CXX_COMPILER_RANLIB": "/usr/bin/gcc-ranlib",
                            "CMAKE_C_COMPILER": "/usr/bin/gcc",
                            "CMAKE_C_COMPILER_AR": "/usr/bin/gcc-ar",
                            "CMAKE_C_COMPILER_RANLIB": "/usr/bin/gcc-ranlib"
                        }
                    }
                ],
                "buildPresets": [
                    {
                        "name": "VSCode",
                        "configurePreset": "VSCode",
                        "jobs": 4
                    }
                ]
            },
            "conanProfile": {
                "name": "devops_profile",
                "include": "default",
                "settings": {
                    "build_type": "Release",
                    "compiler.version": "10"
                },
                "conf": {
                    "tools.build:jobs": 4,
                    "tools.build:compiler_executables": "{'c': '/usr/bin/gcc', 'cpp': '/usr/bin/g++'}"
                }
            }
        }


    @patch("builtins.open", new_callable=mock_open)
    def test_create_devops_profile(self, mock_open):
        # Call the function with the test data
        create_devops_profile(self.parameter_array)

        # Check that open was called correctly
        mock_open.assert_called_once_with("devops_profile.json", 'w')

        # Extract the file handle to check its write calls
        handle = mock_open()

        # Concatenate all the write calls to form the full content
        # Concatenate Write Calls: Since json.dump writes in chunks, the write method is called 
        # multiple times. We concatenate these calls to reconstruct the complete JSON content.
        written_content = ''.join(call_args[0][0] for call_args in handle.write.call_args_list)

        # Convert the written JSON string to a dictionary
        actual_profile = json.loads(written_content)

        # Assert the profile content matches expected
        self.assertEqual(actual_profile, self.expected_profile)


if __name__ == '__main__':
    unittest.main()
