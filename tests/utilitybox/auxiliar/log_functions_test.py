import logging
import unittest
from unittest.mock import patch

from src.utilitybox.auxiliar.log_functions import formatting_log, update_file_log


class TestLoggingFunctions(unittest.TestCase):
    """
    Unit tests for the Logging Functions module.
    """

    @patch('logging.basicConfig')
    def test_formatting_log(self, mock_basic_config):
        """
        Test the formatting_log function.

        This function checks if the 'formatting_log' method correctly calls 'logging.basicConfig'
        with the provided file path, format, and default settings.
        """
        file_path = '/path/to/logfile.log'
        provided_format = '%(asctime)s %(levelname)s: %(message)s'

        formatting_log(file_path, provided_format)

        mock_basic_config.assert_called_once_with(
            force=True,
            filename=file_path,
            format=provided_format,
            level=logging.INFO,
            datefmt='%d/%m/%Y %H:%M:%S'
        )


if __name__ == '__main__':
    unittest.main()
