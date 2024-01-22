import unittest
from unittest.mock import patch
from pathlib import Path
import os

from src.utilitybox.auxiliar.project_paths import get_system_path, get_project_folder, get_project_keys_path, get_project_icons_path


class TestProjectPaths(unittest.TestCase):
    """
    Unit tests for the Project Paths module.
    """

    @patch('os.path.expanduser', return_value='/mocked/user/home')
    def test_get_system_path(self, mock_expanduser):
        """
        Test the get_system_path function.

        This function checks if the get_system_path method correctly combines the user home directory and 'Desktop'.
        """
        system_path = get_system_path()
        expected_path = os.path.join('/mocked/user/home', 'Desktop')
        self.assertEqual(system_path, expected_path)

    def test_get_project_folder(self):
        """
        Test the get_project_folder function.

        This function checks if the get_project_folder method correctly returns the project folder path.
        """
        project_folder = get_project_folder()
        expected_path = Path(__file__).resolve().parent.parent.parent.parent
        self.assertEqual(project_folder, expected_path)

    @patch('src.utilitybox.auxiliar.project_paths.get_project_folder', return_value='/mocked/project/folder')
    def test_get_project_keys_path(self, mock_get_project_folder):
        """
        Test the get_project_keys_path function.

        This function checks if the get_project_keys_path method correctly combines the project folder path,
        'resources', 'results', and 'keys'.
        """
        project_keys_path = get_project_keys_path()
        expected_path = os.path.join('/mocked/project/folder', 'resources', 'results', 'keys')
        self.assertEqual(project_keys_path, expected_path)

    @patch('src.utilitybox.auxiliar.project_paths.get_project_folder', return_value='/mocked/project/folder')
    def test_get_project_icons_path(self, mock_get_project_folder):
        """
        Test the get_project_icons_path function.

        This function checks if the get_project_icons_path method correctly combines the project folder path,
        'resources', and 'icons'.
        """
        project_icons_path = get_project_icons_path()
        expected_path = os.path.join('/mocked/project/folder', 'resources', 'icons')
        self.assertEqual(project_icons_path, expected_path)


if __name__ == '__main__':
    unittest.main()
