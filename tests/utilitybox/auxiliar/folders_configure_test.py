import unittest
from unittest.mock import patch

from src.utilitybox.auxiliar.folders_configure import FoldersConfigure


class TestFoldersConfigure(unittest.TestCase):
    """
    Unit tests for the Folder Configure module.
    """

    @patch('os.path.exists', return_value=True)
    def test_check_folders_setup_existing_folders(self, mock_exists):
        """
        Test the check_folders_setup method when existing folders are present.

        This method checks the existence of default folders and ensures that the corresponding
        'os.path.exists' calls are made.
        """
        folders_configure = FoldersConfigure()
        folders_configure.check_folders_setup()

        mock_exists.assert_any_call(folders_configure.generate_default_results_folder_path())
        mock_exists.assert_any_call(folders_configure.generate_default_logs_folder_path())
        mock_exists.assert_any_call(folders_configure.generate_default_year_folder_path())
        mock_exists.assert_any_call(folders_configure.generate_default_month_folder_path())
        mock_exists.assert_any_call(folders_configure.generate_default_keys_folder_path())

    @patch('os.path.exists', side_effect=[False, False, False, False, False])
    @patch('os.mkdir')
    def test_check_folders_setup_missing_folders(self, mock_mkdir, mock_exists):
        """
        Test the check_folders_setup method when some folders are missing.

        This method checks the existence of default folders and ensures that missing folders
        are created by checking the 'os.path.exists' and 'os.mkdir' calls.
        """
        folders_configure = FoldersConfigure()
        folders_configure.check_folders_setup()

        mock_exists.assert_any_call(folders_configure.generate_default_results_folder_path())
        mock_exists.assert_any_call(folders_configure.generate_default_logs_folder_path())
        mock_exists.assert_any_call(folders_configure.generate_default_year_folder_path())
        mock_exists.assert_any_call(folders_configure.generate_default_month_folder_path())
        mock_exists.assert_any_call(folders_configure.generate_default_keys_folder_path())

        mock_mkdir.assert_any_call(folders_configure.generate_default_results_folder_path())
        mock_mkdir.assert_any_call(folders_configure.generate_default_logs_folder_path())
        mock_mkdir.assert_any_call(folders_configure.generate_default_year_folder_path())
        mock_mkdir.assert_any_call(folders_configure.generate_default_month_folder_path())
        mock_mkdir.assert_any_call(folders_configure.generate_default_keys_folder_path())

    @patch('os.path.exists', return_value=True)
    def test_give_log_name(self, mock_exists):
        """
        Test the give_log_name method.

        This method tests the 'give_log_name' method of FoldersConfigurer and ensures that
        the returned log name is a string and ends with '_ublog.txt'.
        """
        folders_configure = FoldersConfigure()
        log_name = folders_configure.give_log_name()

        self.assertIsInstance(log_name, str)
        self.assertTrue(log_name.endswith('_ublog.txt'))


if __name__ == '__main__':
    unittest.main()
