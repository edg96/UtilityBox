import os.path
import logging

from src.utilitybox.auxiliar.configure_log import LogConfigurer


def formatting_log(file_path: str, provided_format: str) -> None:
    """
    Formatting the logging details and deciding what information to store and in which manner.

    Parameters:
        file_path (str): The path to the log file.
        provided_format (str): The format of the logged information.

    Returns:
        None
    """
    logging.basicConfig(force=True, filename=file_path, format=provided_format, level=logging.INFO,
                        datefmt='%d/%m/%Y %H:%M:%S')


def update_file_log(log_message: str, operation_specific_indentifier: str) -> None:
    """
    Updates the log file associated with the operation type where the log message originates.

    Parameters:
        log_message (str): The message to be logged in the file.
        operation_specific_identifier (str): The operation identifier that specifies the type of operation.
            Must be specified in order for the function to know on which folder to log the message:
            - Example 1: operation identifier = "Search"
              File destination: Year => Month => Search => DD_ublog.log
            - Example 2: operation identifier = "Rename"
              File destination: Year => Month => Rename => DD_ublog.log

    Returns:
        None
    """
    log_configurer = LogConfigurer()
    file_name = log_configurer.give_log_name()
    file_path = os.path.join(log_configurer.get_month_folder_path(), operation_specific_indentifier, file_name)
    formatting_log(file_path, '%(asctime)s %(levelname)s: %(message)s')
    logging.info(log_message)
