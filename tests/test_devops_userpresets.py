import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json

from config_management.user_presets import UserPresets

class TestUserPresets(unittest.TestCase):
    def setUp(self):
        self.mock_json_data = {
            "settings_ide": {
                "theme": "dark",
                "font_size": 14
            },
            "settings_compiler": {
                "optimization": "O2",
                "warnings": "all"
            },
            "settings_build": {
                "parallel_builds": 4,
                "target": "release"
            }
        }
        self.json_string = json.dumps(self.mock_json_data)
        
    @patch('os.getcwd', return_value='/mock/path')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "settings_ide": {"theme": "dark", "font_size": 14},
        "settings_compiler": {"optimization": "O2", "warnings": "all"},
        "settings_build": {"parallel_builds": 4, "target": "release"}
    }))
    def test_init_loads_json(self, mock_file, mock_getcwd):
        # Instantiate UserPresets
        presets = UserPresets()

        # Check if the json dict is correctly loaded
        self.assertEqual(presets.presets_dict, self.mock_json_data)
    
    @patch('os.getcwd', return_value='/mock/path')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "settings_ide": {"theme": "dark", "font_size": 14},
        "settings_compiler": {"optimization": "O2", "warnings": "all"},
        "settings_build": {"parallel_builds": 4, "target": "release"}
    }))
    def test_get_ide_settings(self, mock_file, mock_getcwd):
        # Instantiate UserPresets
        presets = UserPresets()

        # Test get_ide_settings method
        ide_settings = presets.get_ide_settings()
        self.assertEqual(ide_settings, self.mock_json_data["settings_ide"])

    @patch('os.getcwd', return_value='/mock/path')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "settings_ide": {"theme": "dark", "font_size": 14},
        "settings_compiler": {"optimization": "O2", "warnings": "all"},
        "settings_build": {"parallel_builds": 4, "target": "release"}
    }))
    def test_get_compiler_settings(self, mock_file, mock_getcwd):
        # Instantiate UserPresets
        presets = UserPresets()

        # Test get_compiler_settings method
        compiler_settings = presets.get_compiler_settings()
        self.assertEqual(compiler_settings, self.mock_json_data["settings_compiler"])
    
    @patch('os.getcwd', return_value='/mock/path')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "settings_ide": {"theme": "dark", "font_size": 14},
        "settings_compiler": {"optimization": "O2", "warnings": "all"},
        "settings_build": {"parallel_builds": 4, "target": "release"}
    }))
    def test_get_build_settings(self, mock_file, mock_getcwd):
        # Instantiate UserPresets
        presets = UserPresets()

        # Test get_build_settings method
        build_settings = presets.get_build_settings()
        self.assertEqual(build_settings, self.mock_json_data["settings_build"])


    # @patch('os.getcwd', return_value='/mock/path')
    # @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({}))
    # def test_get_compiler_settings_key_error(self, mock_file, mock_getcwd):
    #     # Instantiate UserPresets
    #     presets = UserPresets()

    #     # Test get_compiler_settings method when key is not present
    #     compiler_settings = presets.get_compiler_settings()
    #     self.assertIsNone(compiler_settings)

    # @patch('os.getcwd', return_value='/mock/path')
    # @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({}))
    # def test_get_build_settings_key_error(self, mock_file, mock_getcwd):
    #     # Instantiate UserPresets
    #     presets = UserPresets()

    #     # Test get_build_settings method when key is not present
    #     build_settings = presets.get_build_settings()
    #     self.assertIsNone(build_settings)

# Run the tests
if __name__ == '__main__':
    unittest.main()