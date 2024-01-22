import unittest
from unittest.mock import patch

from src.utilitybox.auxiliar.operations_messages import (
    log_basic_operation_results,
    log_compressing_results,
    log_decompressing_results,
)


class TestOperationsMessages(unittest.TestCase):
    """
    Unit tests for the Operations Messages module.
    """

    @patch('src.utilitybox.auxiliar.operations_messages.update_file_log')
    def test_log_basic_operation_results(self, mock_update_file_log):
        """
        Test the log_basic_operation_results function.

        This function checks if the log_basic_operation_results method correctly calls 'update_file_log'
        with the expected log message and operation specific identifier.
        """
        operation_specific_identifier = 'search'
        results_id = 200
        list_of_files = {'.txt': ['file1.txt', 'file2.txt']}

        log_basic_operation_results(operation_specific_identifier, results_id, list_of_files)

        expected_log_message = (
            '[SEARCH: 200]:\n\tFound the following files:'
            '\n\t\tFiles of type: .txt\n\t\t\tfile1.txt\n\t\t\tfile2.txt'
        )
        mock_update_file_log.assert_called_once_with(expected_log_message, operation_specific_identifier)

    @patch('src.utilitybox.auxiliar.operations_messages.update_file_log')
    @patch('src.utilitybox.auxiliar.project_paths.get_system_path', return_value="/default/destination")
    def test_log_compressing_results(self, mock_get_system_path, mock_update_file_log):
        """
        Test the log_compressing_results function.

        This function checks if the log_compressing_results method correctly calls 'update_file_log'
        with the expected log message and operation specific identifier.
        """
        operation_specific_identifier = 'compress'
        operation_id = 200
        destination_path = '/custom/destination'

        log_compressing_results(operation_specific_identifier, operation_id, destination_path)

        expected_log_message = (
            '[COMPRESS: 200]:'
            '\n\tArchive created at the following location:'
            '\n\t\t/custom/destination'
        )
        mock_update_file_log.assert_called_once_with(expected_log_message, operation_specific_identifier)

    @patch('src.utilitybox.auxiliar.operations_messages.update_file_log')
    @patch('src.utilitybox.auxiliar.project_paths.get_system_path', return_value="/default/destination")
    def test_log_decompressing_results(self, mock_get_system_path, mock_update_file_log):
        """
        Test the log_decompressing_results function.

        This function checks if the log_decompressing_results method correctly calls 'update_file_log'
        with the expected log message and operation unique identifier.
        """
        operation_unique_identifier = 'decompress'
        operation_id = 204
        destination_path = '/custom/destination'

        log_decompressing_results(operation_unique_identifier, operation_id, destination_path)

        expected_log_message = (
            '[DECOMPRESS: 204]:'
            '\n\tDecompressed the files in following location:'
            '\n\t\t/custom/destination'
        )
        mock_update_file_log.assert_called_once_with(expected_log_message, operation_unique_identifier)


if __name__ == '__main__':
    unittest.main()
