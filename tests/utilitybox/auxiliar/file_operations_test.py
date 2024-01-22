import unittest
from unittest.mock import Mock, patch
from src.utilitybox.auxiliar.file_operations import browse_folder, browse_file, browse_multiple_files


class TestFileOperations(unittest.TestCase):
    """
    Unit tests for the File Operations module.
    """

    @patch('tkinter.filedialog.askdirectory', return_value='/path/to/folder')
    def test_browse_folder(self, mock_askdirectory):
        """
        Test the browse_folder function.

        This function simulates browsing for a folder and updating an entry widget with the selected folder path.
        """
        entry_widget = Mock()

        browse_folder(entry_widget)

        entry_widget.delete.assert_called_once_with(0, 'end')
        entry_widget.insert.assert_called_once_with(0, '/path/to/folder')

    @patch('tkinter.filedialog.askopenfilename', return_value='/path/to/file.txt')
    def test_browse_file(self, mock_askopenfilename):
        """
        Test the browse_file function.

        This function simulates browsing for a file and updating an entry widget with the selected file path.
        """
        entry_widget = Mock()

        browse_file(entry_widget)

        entry_widget.delete.assert_called_once_with(0, 'end')
        entry_widget.insert.assert_called_once_with(0, '/path/to/file.txt')

    @patch('tkinter.filedialog.askopenfilenames', return_value=('/path/to/file1.txt', '/path/to/file2.txt'))
    def test_browse_multiple_files(self, mock_askopenfilenames):
        """
        Test the browse_multiple_files function.

        This function simulates browsing for multiple files and returns a list of selected file paths.
        """
        files = browse_multiple_files()

        self.assertEqual(files, ['/path/to/file1.txt', '/path/to/file2.txt'])


if __name__ == '__main__':
    unittest.main()
