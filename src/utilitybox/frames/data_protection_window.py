import os
import tkinter as tk

import customtkinter as ctk

from src.utilitybox.auxiliar import log_functions, reusable_functions
from src.utilitybox.functionalities.decryption import Decryption
from src.utilitybox.functionalities.encryption import Encryption
from src.utilitybox.auxiliar.path_validator import check_path_existence

"""
File encryption parameters (used for radio buttons).
"""
ENCRYPTION_OPTION = 1
DECRYPTION_OPTION = 2


def _log_encryption_result(operation_specific_identifier: str, operation_id: int, file_key_pair: dict[str, str]) -> None:
    """
    Log the result of an encryption operation.

    Parameters:
        operation_specific_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): The operation's status code (200 for success, 204 for no content, 404 for error).
        file_key_pair (dict[str, str]): A dictionary containing file names as keys and key paths as values.
    """
    log_file_message = (f'[{operation_specific_identifier.upper()}: {operation_id}]:'
                        f'\nEncrypted the following file:')
    for file_name, key_path in file_key_pair.items():
        log_file_message += f'\n\t{file_name}'
        log_file_message += '\nKey saved in the following location:'
        log_file_message += f'\n\t{key_path}'

    log_functions.update_file_log(log_file_message, operation_specific_identifier)


def _perform_encryption(mainbox, operation_specific_identifier: str, file_path: str) -> None:
    """
    Perform file encryption.

    Parameters:
        mainbox (MainBox): An instance of the MainBox class.
        operation_specific_identifier (list): A list of operation identifiers for logging.
        file_path (str): The path of the file to be encrypted.
    """
    operation_code = {'OK': 200, 'BAD REQUEST': 404}

    operation_id = operation_code['BAD REQUEST']
    if not check_path_existence(file_path):
        log_message = reusable_functions.path_invalid_message(operation_specific_identifier, operation_id, file_path)
        log_functions.update_file_log(log_message, operation_specific_identifier)
        reusable_functions.update_display_log(mainbox, operation_specific_identifier, operation_id)
        return

    operation_id = operation_code['OK']
    try:
        encryption = Encryption(file_path)
        encryption.generate_key()
        key = encryption.load_key()
        encryption.encrypt_file(key)

        reusable_functions.update_display_log(mainbox, operation_specific_identifier, operation_id)
        _log_encryption_result(operation_specific_identifier, operation_id, encryption.file_key_pair)
    except Exception as e:
        print(e)


def _log_decryption_result(operation_specific_identifier: str, operation_id: int, file_key_pair: dict[str, str]) -> None:
    """
    Log the result of an decryption operation.

    Parameters:
        operation_specific_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): The operation's status code (200 for success, 204 for no content, 404 for error).
        file_key_pair (dict[str, str]): A dictionary containing file names as keys and key paths as values.
    """
    log_file_message = (f'[{operation_specific_identifier.upper()}: {operation_id}]:'
                        f'\nDecrypted the following file:')
    for file_name, key_path in file_key_pair.items():
        log_file_message += f'\n\t{file_name}'
        log_file_message += '\nKey from the folowing location deleted:'
        log_file_message += f'\n\t{key_path}'

    log_functions.update_file_log(log_file_message, operation_specific_identifier)


def _perform_decryption(mainbox, operation_specific_identifier: str, file_path: str) -> None:
    """
    Perform file decryption.

    Parameters:
        mainbox (MainBox): An instance of the MainBox class.
        operation_specific_identifier (list): A list of operation identifiers for logging.
        file_path (str): The path of the file to be encrypted.
    """
    operation_code = {'OK': 200, 'BAD REQUEST': 404}

    operation_id = operation_code['BAD REQUEST']
    if not check_path_existence(file_path):
        log_message = reusable_functions.path_invalid_message(operation_specific_identifier, operation_id, file_path)
        log_functions.update_file_log(log_message, operation_specific_identifier)
        reusable_functions.update_display_log(mainbox, operation_specific_identifier, operation_id)
        return

    operation_id = operation_code['OK']
    try:
        decryption = Decryption(file_path)
        key = decryption.load_key()
        decryption.decrypt_file(key)

        reusable_functions.update_display_log(mainbox, operation_specific_identifier, operation_id)
        _log_decryption_result(operation_specific_identifier, operation_id, decryption.file_key_pair)
    except Exception as e:
        print(e)


def _start_process(mainbox, operation_specific_identifier: list[str], radio_option: int, file_path: str) -> None:
    """
    Start the encryption or decryption process based the user selection.

    Parameters:
        mainbox (MainBox): An instance of the MainBox class.
        operation_specific_identifier (str): The operation identifier that specifies the type of operation(s).
        radio_option (int): An integer representing the selected option (1 for Encryption, 2 for Decryption).
        file_path (str): The path of the file to be processed.
    """
    if radio_option == ENCRYPTION_OPTION:
        _perform_encryption(mainbox, operation_specific_identifier[0], file_path)
    elif radio_option == DECRYPTION_OPTION:
        _perform_decryption(mainbox, operation_specific_identifier[1], file_path)


class DataProtectionWindow(ctk.CTkToplevel):
    def __init__(self, mainbox):
        """
        Create a window for the data protection functionality.

        Parameters:
            mainbox (MainBox): An instance of the MainBox class that contain usefull information
                used for different functions in order to keep the main window up to date.

        Notes:
            The window will not close after the search is performed.
            The user can edit and modify the values as needed.
            The window must be closed manually.
        """
        super().__init__()
        self.title(' Data protection')
        self.geometry('254x354')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.operation_specific_identifier = ['Encryption', 'Decryption']
        self.radio_current_option = 0
        self.after(250, lambda: self.iconbitmap(
            (os.path.join(reusable_functions.get_project_icons_path(), 'DataProtection.ico'))))

        # Widgets functions and variables
        def radiobutton_event():
            self.radio_current_option = radio_var.get()

        radio_var = tk.IntVar(value=0)

        # Widgets implementation
        # Encryption
        self.encryption_radiobutton = ctk.CTkRadioButton(
            master=self, text='Encryption',
            command=radiobutton_event, variable=radio_var, value=1)

        # Decryption
        self.decryption_radiobutton = ctk.CTkRadioButton(
            master=self, text='Decryption',
            command=radiobutton_event, variable=radio_var, value=2)

        self.file_path_text = ctk.CTkLabel(master=self, text='Enter the file path: ')
        self.file_path_entry = ctk.CTkEntry(master=self, width=220)
        self.file_path_button = ctk.CTkButton(
            master=self, text='Browse file', font=('Helvetica', 12, 'bold'), fg_color='#00539C', text_color='white',
            command=lambda: reusable_functions.browse_file(self.file_path_entry))

        # Action button
        self.start_process_button = ctk.CTkButton(
            master=self, text='Start process', font=('Helvetica', 12, 'bold'), fg_color='green', text_color='white',
            command=lambda: _start_process(mainbox, self.operation_specific_identifier, self.radio_current_option,
                                           self.file_path_entry.get()))

        # Widgets placement
        self.encryption_radiobutton.grid(row=1, column=0, padx=(16, 0), pady=(15, 0), sticky='nw')
        self.decryption_radiobutton.grid(row=2, column=0, padx=(16, 0), pady=(20, 0), sticky='nw')
        self.file_path_text.grid(row=3, column=0, padx=(16, 0), pady=(35, 0))
        self.file_path_entry.grid(row=4, column=0, padx=(16, 0), pady=(35, 0))
        self.file_path_button.grid(row=5, column=0, padx=(16, 0), pady=(35, 0))

        self.start_process_button.grid(row=6, column=0, padx=(16, 0), pady=(40, 0))
