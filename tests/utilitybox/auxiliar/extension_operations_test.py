import unittest

from src.utilitybox.auxiliar.extension_operations import split_extensions, group_files_by_extensions


class TestExtensionOperations(unittest.TestCase):
    """
    Unit tests for the Extension Operations module.
    """

    def test_split_extensions(self):
        """
        Test the split_extensions function.

        This function extracts extensions from a comma-separated string input.
        """
        input_extensions = 'txt,  csv , pdf,  jpg'
        expected_output = ['txt', 'csv', 'pdf', 'jpg']

        result = split_extensions(input_extensions)

        self.assertEqual(result, expected_output)

    def test_group_files_by_extensions(self):
        """
        Test the group_files_by_extensions function.

        This function extracts extensions from a list of files and groups them accordingly.
        """
        list_of_files = [
            'document1.txt',
            'document2.txt',
            'data.csv',
            'image.jpg',
            'presentation.pptx',
            'archive.zip',
        ]
        expected_output = {
            'txt': ['document1', 'document2'],
            'csv': ['data'],
            'jpg': ['image'],
            'pptx': ['presentation'],
            'zip': ['archive'],
        }

        result = group_files_by_extensions(list_of_files)

        self.assertEqual(result, expected_output)

    def test_split_extensions_empty_input(self):
        """
        Test the split_extensions function with an empty input.

        An empty input should result in an empty list.
        """
        input_extensions = ''
        expected_output = ['']

        result = split_extensions(input_extensions)

        self.assertEqual(result, expected_output)

    def test_group_files_by_extensions_empty_input(self):
        """
        Test the group_files_by_extensions function with an empty input list.

        An empty input list should result in an empty dictionary.
        """
        list_of_files = []
        expected_output = {}

        result = group_files_by_extensions(list_of_files)

        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
