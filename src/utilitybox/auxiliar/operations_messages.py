import os

from src.utilitybox.auxiliar.log_functions import update_file_log
from src.utilitybox.auxiliar.project_paths import get_system_path


def log_basic_operation_results(operation_specific_identifier: str, results_id: int,
                                list_of_files: dict[str, list[str]]) -> None:
    """
    Log the results of deleting files by single or multiple extensions.

    Params:
        operation_specific_identifier (str): The identifier for the deletion operation.
        results_id (int): The operation's status code (200 for success, 204 for no content, 404 for error).
        list_of_files (dict[str, list[str]]): A dictionary containing the results files grouped by extension.
    """
    if operation_specific_identifier.lower() == 'search':
        operation_results_keyword = 'Found'
    elif operation_specific_identifier.lower() == 'sort':
        operation_results_keyword = 'Sorted'
    else:
        operation_results_keyword = 'Deleted'

    log_file_message = f'[{operation_specific_identifier.upper()}: {results_id}]:\n\t{operation_results_keyword} the following files:'

    if not list_of_files:
        log_file_message += '\n\t\tNone'
    else:
        for extension, files in list_of_files.items():
            log_file_message += f'\n\t\tFiles of type: {extension}'
            for file in files:
                log_file_message += f'\n\t\t\t{os.path.basename(file)}'

    update_file_log(log_file_message, operation_specific_identifier)


def log_compressing_results(operation_specific_identifier: str, operation_id: int, destination_path: str) -> None:
    """
    Log the results of a compression operation.

    Params:
        operation_specific_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): The operation's status code (200 for success, 204 for no content, 404 for error).
        destination_path (str): The destination path where the archive is created.
    """
    if not destination_path:
        destination_path = get_system_path()
    log_file_message = (f'[{operation_specific_identifier.upper()}: {operation_id}]:'
                        f'\n\tArchive created at the following location:'
                        f'\n\t\t{destination_path}')
    update_file_log(log_file_message, operation_specific_identifier)


def log_decompressing_results(operation_unique_identifier: str, operation_id: int, destination_path: str) -> None:
    """
    Log the results of a decompression operation.

    Params:
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): The operation's status code (200 for success, 204 for no content, 404 for error).
        destination_path (str): The destination path where the files are decompressed.
    """
    if not destination_path:
        destination_path = get_system_path()
    log_file_message = (f'[{operation_unique_identifier.upper()}: {operation_id}]:'
                        f'\n\tDecompressed the files in following location:'
                        f'\n\t\t{destination_path}')
    update_file_log(log_file_message, operation_unique_identifier)


def log_encryption_result(operation_specific_identifier: str, operation_id: int, file_key_pair: dict[str, str]) -> None:
    """
    Log the result of an encryption operation.

    Params:
        operation_specific_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): The operation's status code (200 for success, 204 for no content, 404 for error).
        file_key_pair (dict[str, str]): A dictionary containing file names as keys and key paths as values.
    """
    log_file_message = (f'[{operation_specific_identifier.upper()}: {operation_id}]:'
                        f'\n\tEncrypted the following file:')
    for file_name, key_path in file_key_pair.items():
        log_file_message += f'\n\t\t{file_name}'
        log_file_message += '\n\tKey saved in the following location:'
        log_file_message += f'\n\t\t{key_path}'

    update_file_log(log_file_message, operation_specific_identifier)


def log_decryption_result(operation_specific_identifier: str, operation_id: int, file_key_pair: dict[str, str]) -> None:
    """
    Log the result of a decryption operation.

    Params:
        operation_specific_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): The operation's status code (200 for success, 204 for no content, 404 for error).
        file_key_pair (dict[str, str]): A dictionary containing file names as keys and key paths as values.
    """
    log_file_message = (f'[{operation_specific_identifier.upper()}: {operation_id}]:'
                        f'\n\tDecrypted the following file:')
    for file_name, key_path in file_key_pair.items():
        log_file_message += f'\n\t\t{file_name}'
        log_file_message += '\n\tKey from the following location deleted:'
        log_file_message += f'\n\t\t{key_path}'

    update_file_log(log_file_message, operation_specific_identifier)
