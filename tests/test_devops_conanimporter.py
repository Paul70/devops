import unittest
from unittest.mock import patch, MagicMock
import os

# The ConanImporter class
from config_management.conan_importer import ConanImporter

class TestConanImporter(unittest.TestCase):
    # Unittest patch decorator:
    # Mock relevant objects and functions to be able to test all porperly.
    # Mocks are valid within the following test function.

    @patch('os.getcwd', return_value='/mock/path')
    @patch('config_management.conan_importer.ConanFileLoader')
    def test_import_name_from_conan(self, MockConanFileLoader, mock_getcwd):
        # some testing of mocks
        current_dir = os.getcwd()
        self.assertEqual(current_dir, '/mock/path')

        
        # Create a mock conanfile object
        mock_conanfile = MagicMock()
        mock_conanfile.name = "mock_name"
        mock_conanfile.author = "mock_author"
        mock_conanfile.version = "mock_version"

        # Configure the mock loader to return the mock conanfile
        mock_loader_instance = MockConanFileLoader.return_value
        mock_loader_instance.load_conanfile.return_value = mock_conanfile

        # Instantiate the ConanImporter
        importer = ConanImporter()

        # Test import_name_from_conan method
        name = importer.import_conan_name()
        self.assertEqual(name, "mock_name")

        # Test import_author_from_conan method
        author = importer.import_conan_author()
        self.assertEqual(author, "mock_author")

        # Test import_version_from_conan method
        version = importer.import_conan_version()
        self.assertEqual(version, "mock_version")

if __name__ == '__main__':
    unittest.main()