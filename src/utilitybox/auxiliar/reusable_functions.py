import os
import tkinter
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk


# Project path operations
def get_system_path() -> str:
    """
    Get the system's default path for file operations (usually the desktop).

    Returns:
        str: The default system path.
    """
    return os.path.join(os.path.expanduser('~'), 'Desktop')


def get_project_logs_path() -> Path:
    """
    Get the root path of the project where this script is located for log files.

    Returns:
        Path: The root path of the project's logs directory.
    """
    script_path = Path(__file__).resolve()
    levels_to_main_root = 4
    project_root = script_path

    for _ in range(levels_to_main_root):
        project_root = project_root.parent

    logs_folder = project_root / 'resources' / 'results' / 'logs'

    return logs_folder


def get_project_keys_path() -> Path:
    """
    Get the root path of the project where this script is located for key files.

    Returns:
        Path: The root path of the project's keys directory.
    """
    script_path = Path(__file__).resolve()
    levels_to_main_root = 4
    project_root = script_path

    for _ in range(levels_to_main_root):
        project_root = project_root.parent

    logs_folder = project_root / 'resources' / 'results' / 'keys'

    return logs_folder


def get_project_icons_path() -> Path:
    """
    Get the root path of the project where this script is located for icon files.

    Returns:
        Path: The root path of the project's icons directory.
    """
    script_path = Path(__file__).resolve()
    levels_to_main_root = 4
    project_root = script_path

    for _ in range(levels_to_main_root):
        project_root = project_root.parent

    icons_folder = project_root / 'resources' / 'icons'

    return icons_folder


def get_currency_path() -> Path:
    """
    Get the root path of the project where this script is located for icon files.

    Returns:
        Path: The root path of the project's icons directory.
    """
    script_path = Path(__file__).resolve()
    levels_to_main_root = 4
    project_root = script_path

    for _ in range(levels_to_main_root):
        project_root = project_root.parent

    icons_folder = project_root / 'resources' / 'files'

    return icons_folder


# Operation messages
def success_message(operation_unique_identifier: str, operation_id: int) -> str:
    """
    Generates a success message and returns it as a string.

    Parameters:
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): A HTTP code indicating the state of the result of the operation.

    Returns:
        str: A message containing the type of operation, a HTTP type response code, and the number of files found.
    """
    if operation_id == 200:
        return (f'[{operation_unique_identifier.upper()} {operation_id}]:'
                f'\nSuccess: changes performed.')
    elif operation_id == 204:
        return (f'[{operation_unique_identifier.upper()} {operation_id}]:'
                f'\nSuccess: no changes performed.')


def path_invalid_message(operation_unique_identifier: str, operation_id: int, location_path: str = '') -> str:
    """
    Construct a detailed result message to be logged, indicating an invalid path.

    Parameters:
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): A HTTP code indicating the state of the result of the operation.
        location_path (str): The path of a file or folder where the operation takes place.

    Returns:
        str: A message indicating an invalid path.
    """
    if not location_path:
        return (f'[{operation_unique_identifier.upper()}: {operation_id}]:'
                f'\nInvalid path:'
                f'\n\tEmpty path')
    else:
        return (f'[{operation_unique_identifier.upper()}: {operation_id}]:'
                f'\nInvalid path:'
                f'\n\t{location_path}')


def simple_success_message(operation_unique_identifier: str, operation_id: int) -> str:
    """
    Generates a simplified success message and returns it as a string.

    Parameters:
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): A HTTP code indicating the state of the result of the operation.

    Returns:
        str: A simplified success message.
    """
    if operation_id == 200:
        return (f'[{operation_unique_identifier.upper()} {operation_id}]: Success: changes performed')
    elif operation_id == 204:
        return (f'[{operation_unique_identifier.upper()} {operation_id}]: Success: no changes performed')


def simple_path_invalid_message(operation_unique_identifier: str, operation_id: int) -> str:
    """
    Construct a simplified result message to be logged, indicating an invalid path.

    Parameters:
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): A HTTP code indicating the state of the result of the operation.

    Returns:
        str: A simplified message indicating an invalid path.
    """
    return (f'[{operation_unique_identifier.upper()}: {operation_id}]: Failure: Invalid path')


def update_display_log(mainbox, operation_unique_identifier: str, operation_id: int) -> None:
    """
    Construct a message based on an operation id (HTTP codes association) and pass it to the MainBox
    widget to be displayed to the user.

    Parameters:
        mainbox (MainBox): An instance of the MainBox class (parent).
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): A HTTP code indicating the state of the result of the operation.

    Returns:
        None
    """
    log_frame_message, operation_status_color = '', ''

    if operation_id == 200:
        operation_status_color = '#009137'
        log_frame_message = simple_success_message(operation_unique_identifier, operation_id)
    elif operation_id == 204:
        operation_status_color = '#006571'
        log_frame_message = simple_success_message(operation_unique_identifier, operation_id)
    elif operation_id == 404:
        operation_status_color = '#912800'
        log_frame_message = simple_path_invalid_message(operation_unique_identifier, operation_id)

    mainbox.update_log(log_frame_message, operation_status_color)


# Folders/ files operations
def browse_folder(entry_widget: ctk.CTkEntry) -> None:
    """
    Open a file dialog to browse and select a folder.

    Parameters:
        entry_widget (tk.Entry): The entry widget where the selected folder path will be displayed.

    Returns:
        None
    """
    folder_path = tkinter.filedialog.askdirectory()
    if folder_path:
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, folder_path)


def browse_file(entry_widget: ctk.CTkEntry) -> None:
    """
    Open a file dialog to browse and select a file.

    Parameters:
        entry_widget (tk.Entry): The entry widget where the selected file path will be displayed.

    Returns:
        None
    """
    file_path = tkinter.filedialog.askopenfilename()
    if file_path:
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, file_path)


def browse_multiple_files() -> list[str]:
    """
    Open a file dialog to browse and select multiple files.

    Returns:
        list[str]: A list of selected file paths.
    """
    files = tkinter.filedialog.askopenfilenames()
    return list(files)


def read_from_file(file_path: str, mode: str = 'r') -> str:
    """
    Read content from a file.

    Parameters:
        file_path (str): The path to the file.
        mode (str, optional): The mode in which the file should be opened. Defaults to 'r' (read).

    Returns:
        str: The content read from the file.
    """
    try:
        with open(file_path, mode) as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f'File not found: {file_path}')

    return file_content


def read_from_file_by_line(file_path: str, mode: str = 'r') -> str:
    """
    Read content from a file.

    Parameters:
        file_path (str): The path to the file.
        mode (str, optional): The mode in which the file should be opened. Defaults to 'r' (read).

    Returns:
        str: The content read from the file.
    """
    try:
        with open(file_path, mode) as file:
            file_content = file.read().splitlines()
    except FileNotFoundError:
        print(f'File not found: {file_path}')

    return file_content


def write_to_file(file_path: str, content: str | bytes, mode: str = 'w'):
    """
    Write content to a file.

    Parameters:
        file_path (str): The path to the file.
        content (str | bytes): The content to write to the file.
        mode (str, optional): The mode in which the file should be opened. Defaults to 'w' (write).

    Returns:
        None
    """
    try:
        with open(file_path, mode) as file:
            file.write(content)
    except FileNotFoundError:
        print(f'File not found: {file_path}')


# Extensions split
def split_extensions(list_of_file_extensions: str) -> list[str]:
    """
    Split a string of file extensions separated by commas into a list of extensions.

    Parameters:
        list_of_file_extensions (str): A string of file extensions separated by commas.

    Returns:
        list[str]: A list of cleaned file extensions.
    """
    cleaned_list_of_file_extensions = []
    new_found_extension = ''
    for letter in list_of_file_extensions:
        if letter != ',':
            new_found_extension += letter
        else:
            cleaned_list_of_file_extensions.append(new_found_extension.replace(' ', ''))
            new_found_extension = ''
    cleaned_list_of_file_extensions.append(new_found_extension.replace(' ', ''))

    return cleaned_list_of_file_extensions
