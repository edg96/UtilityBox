import unittest
from unittest.mock import patch

from src.utilitybox.auxiliar.log_messages import (
    convert_slashes,
    success_message,
    path_invalid_message,
    simple_success_message,
    simple_path_invalid_message,
    update_display_log
)


class TestLogMessages(unittest.TestCase):
    """
    Unit tests for the Log Messages module.
    """

    def test_convert_slashes(self):
        """
        Test the convert_slashes function.

        This function checks if the function correctly converts forward slashes to backslashes.
        """
        input_path = 'C:/path/to/file'
        expected_output = 'C:\\path\\to\\file'
        self.assertEqual(convert_slashes(input_path), expected_output)

    def test_success_message(self):
        """
        Test the success_message function.

        This function checks if the function correctly generates success messages based on the provided parameters.
        """
        operation_unique_identifier = 'search'
        operation_id_200 = 200
        operation_id_204 = 204

        expected_output_200 = '[SEARCH: 200]:\nSuccess: changes performed.'
        expected_output_204 = '[SEARCH: 204]:\nSuccess: no changes performed.'

        self.assertEqual(success_message(operation_unique_identifier, operation_id_200), expected_output_200)
        self.assertEqual(success_message(operation_unique_identifier, operation_id_204), expected_output_204)

    def test_path_invalid_message(self):
        """
        Test the path_invalid_message function.

        This function checks if the function correctly generates path invalid messages based on the provided parameters.
        """
        operation_unique_identifier = 'delete'
        operation_id_200 = 200
        operation_id_204 = 204
        location_path = 'C:/invalid/path'

        expected_output_200 = '[DELETE: 200]:\n\tInvalid path:\n\t\tEmpty path'
        expected_output_204 = '[DELETE: 204]:\n\tInvalid path:\n\t\tC:\\invalid\\path'

        self.assertEqual(path_invalid_message(operation_unique_identifier, operation_id_200), expected_output_200)
        self.assertEqual(path_invalid_message(operation_unique_identifier, operation_id_204, location_path), expected_output_204)

    def test_simple_success_message(self):
        """
        Test the simple_success_message function.

        This function checks if the function correctly generates simple success messages based on the provided parameters.
        """
        operation_unique_identifier = 'encrypt'
        operation_id_200 = 200
        operation_id_204 = 204

        expected_output_200 = '[ENCRYPT: 200]: Success: changes performed'
        expected_output_204 = '[ENCRYPT: 204]: Success: no changes performed'

        self.assertEqual(simple_success_message(operation_unique_identifier, operation_id_200), expected_output_200)
        self.assertEqual(simple_success_message(operation_unique_identifier, operation_id_204), expected_output_204)

    def test_simple_path_invalid_message(self):
        """
        Test the simple_path_invalid_message function.

        This function checks if the function correctly generates simple path invalid messages based on the provided parameters.
        """
        operation_unique_identifier = 'compress'
        operation_id_404 = 404

        expected_output_404 = '[COMPRESS: 404]: Failure: Invalid path'

        self.assertEqual(simple_path_invalid_message(operation_unique_identifier, operation_id_404), expected_output_404)

    @patch('src.utilitybox.mainbox.MainBox')
    def test_update_display_log(self, mock_mainbox_class):
        """
        Test the update_display_log function.

        This function checks if the function correctly updates the display log based on the provided parameters.
        """
        mainbox_instance = mock_mainbox_class.return_value
        operation_unique_identifier = 'decrypt'
        operation_id_200 = 200
        operation_id_204 = 204
        operation_id_404 = 404

        update_display_log(mainbox_instance, operation_unique_identifier, operation_id_200)
        mainbox_instance.update_log.assert_called_once_with(True, '[DECRYPT: 200]: Success: changes performed', '#009137')

        update_display_log(mainbox_instance, operation_unique_identifier, operation_id_204)
        mainbox_instance.update_log.assert_called_with(True, '[DECRYPT: 204]: Success: no changes performed', '#006571')

        update_display_log(mainbox_instance, operation_unique_identifier, operation_id_404)
        mainbox_instance.update_log.assert_called_with(True, '[DECRYPT: 404]: Failure: Invalid path', '#912800')


if __name__ == '__main__':
    unittest.main()
