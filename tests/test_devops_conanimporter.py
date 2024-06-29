import unittest
from unittest.mock import patch, MagicMock
import os

# The ConanImporter class
from devops.config_management.conan_importer import ConanImporter

class TestConanImporter(unittest.TestCase):
    # Unittest patch decorator:
    # Mock relevant objects and functions to be able to test all porperly.
    # Mocks are valid within the following test function.

    # Patch of os.getcwd method: getcwd always retruns "/mock/path" in this functio context.
    @patch('os.getcwd', return_value='/mock/path')

    @patch('os.path.exists', return_value=True)
    # Patch conans.client.loader.ConanFileLoader: Mock of class ConanFileLoader
    @patch('conans.client.loader.ConanFileLoader')
    def test_import_name_from_conan(self, MockConanFileLoader, mock_exists, mock_getcwd):
        # some testing of mocks
        current_dir = os.getcwd()
        self.assertEqual(current_dir, '/mock/path')

        
        # Create a mock conanfile object
        mock_conanfile = MagicMock()
        mock_conanfile.name = "mock_name"
        #mock_conanfile.author = "mock_author"
        #mock_conanfile.version = "mock_version"

        # Configure the mock loader to return the mock conanfile
        mock_loader_instance = MockConanFileLoader.return_value
        mock_loader_instance.load_conanfile.return_value = mock_conanfile

        # Instantiate the ConanImporter
        importer = ConanImporter()

        # Test import_name_from_conan method
        name = importer.import_name_from_conan()
        self.assertEqual(name, "mock_name")

        # Test import_author_from_conan method
        #author = importer.import_author_from_conan()
        #self.assertEqual(author, "mock_author")

        # Test import_version_from_conan method
        #version = importer.import_version_from_conan()
        #self.assertEqual(version, "mock_version")

if __name__ == '__main__':
    unittest.main()