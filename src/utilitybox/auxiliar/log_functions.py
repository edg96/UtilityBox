import os.path
import logging

from src.utilitybox.auxiliar.folders_configure import FoldersConfigure


def formatting_log(file_path: str, provided_format: str) -> None:
    """
    Formatting the logging details and deciding what information to store and in which manner.

    Params:
        file_path (str): The path to the log file.
        provided_format (str): The format of the logged information.
    """
    logging.basicConfig(force=True, filename=file_path, format=provided_format, level=logging.INFO,
                        datefmt='%d/%m/%Y %H:%M:%S')


def update_file_log(log_message: str, operation_specific_identifier: str) -> None:
    """
    Updates the log file associated with the operation type where the log message originates.

    Params:
        log_message (str): The message to be logged in the file.
        operation_specific_identifier (str): The operation identifier that specifies the type of operation.
            Must be specified in order for the function to know on which folder to log the message:
            - Example 1: operation identifier = "Search"
              File destination: Year => Month => Search => DD_ublog.log
            - Example 2: operation identifier = "Rename"
              File destination: Year => Month => Rename => DD_ublog.log
    """
    folders_configure = FoldersConfigure()
    folders_configure.check_folders_setup()

    file_name = folders_configure.give_log_name()
    months_folder_path = folders_configure.generate_default_month_folder_path()
    file_path = os.path.join(months_folder_path, operation_specific_identifier, file_name)

    formatting_log(file_path, '%(asctime)s %(levelname)s: %(message)s')
    logging.info(log_message)
