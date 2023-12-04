import os
import tkinter as tk

import customtkinter as ctk

from src.utilitybox.auxiliar.file_operations import browse_file
from src.utilitybox.auxiliar.log_functions import update_file_log
from src.utilitybox.auxiliar.operations_messages import log_encryption_result, log_decryption_result
from src.utilitybox.auxiliar.log_messages import path_invalid_message, update_display_log
from src.utilitybox.auxiliar.project_paths import get_project_icons_path
from src.utilitybox.functionalities.decryption import Decryption
from src.utilitybox.functionalities.encryption import Encryption

"""
File encryption Params (used for radio buttons).
"""
ENCRYPTION_OPTION = 1
DECRYPTION_OPTION = 2


def _perform_encryption(mainbox, operation_specific_identifier: str, file_path: str) -> None:
    """
    Perform file encryption.

    Params:
        mainbox (MainBox): An instance of the MainBox class.
        operation_specific_identifier (list): A list of operation identifiers for logging.
        file_path (str): The path of the file to be encrypted.
    """
    operation_code = {'OK': 200, 'BAD REQUEST': 404}

    operation_id = operation_code['BAD REQUEST']
    if not os.path.exists(file_path):
        log_message = path_invalid_message(operation_specific_identifier, operation_id, file_path)
        update_file_log(log_message, operation_specific_identifier)
        update_display_log(mainbox, operation_specific_identifier, operation_id)
        return

    operation_id = operation_code['OK']
    try:
        encryption = Encryption(file_path)
        encryption.generate_key()
        key = encryption.load_key()
        encryption.encrypt_file(key)

        update_display_log(mainbox, operation_specific_identifier, operation_id)
        log_encryption_result(operation_specific_identifier, operation_id, encryption.file_key_pair)
    except Exception as e:
        print(e)


def _perform_decryption(mainbox, operation_specific_identifier: str, file_path: str) -> None:
    """
    Perform file decryption.

    Params:
        mainbox (MainBox): An instance of the MainBox class.
        operation_specific_identifier (list): A list of operation identifiers for logging.
        file_path (str): The path of the file to be encrypted.
    """
    operation_code = {'OK': 200, 'BAD REQUEST': 404}

    operation_id = operation_code['BAD REQUEST']
    if not os.path.exists(file_path):
        log_message = path_invalid_message(operation_specific_identifier, operation_id, file_path)
        update_file_log(log_message, operation_specific_identifier)
        update_display_log(mainbox, operation_specific_identifier, operation_id)
        return

    operation_id = operation_code['OK']
    try:
        decryption = Decryption(file_path)
        key = decryption.load_key()
        decryption.decrypt_file(key)

        update_display_log(mainbox, operation_specific_identifier, operation_id)
        log_decryption_result(operation_specific_identifier, operation_id, decryption.file_key_pair)
    except Exception as e:
        print(e)


def _determine_operation_type(mainbox, operation_specific_identifier: list[str], radio_option: int,
                              file_path: str) -> None:
    """
    Start the encryption or decryption process based on the user selection.

    Params:
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
    """
    Create a window for the data protection functionality.

    Notes:
        The window will not close after the search is performed.
        The user can edit and modify the values as needed.
        The window must be closed manually.
    """

    def __init__(self, mainbox):
        """
        Initialize the DataProtectionWindow object.

        Params:
            mainbox (MainBox): An instance of the MainBox class that contains useful information
                used for different functions to keep the main window up to date.
        """
        super().__init__()
        self.title(' Data protection')
        self.geometry('254x354')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.operation_specific_identifier = ['Encryption', 'Decryption']
        self.radio_current_option = 0
        self.after(250, lambda: self.iconbitmap(
            (os.path.join(get_project_icons_path(), 'DataProtection.ico'))))

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
            command=lambda: browse_file(self.file_path_entry))

        # Action button
        self.start_process_button = ctk.CTkButton(
            master=self, text='Start process', font=('Helvetica', 12, 'bold'), fg_color='green', text_color='white',
            command=lambda: _determine_operation_type(mainbox, self.operation_specific_identifier,
                                                      self.radio_current_option,
                                                      self.file_path_entry.get()))

        # Widgets placement
        self.encryption_radiobutton.grid(row=1, column=0, padx=(16, 0), pady=(15, 0), sticky='nw')
        self.decryption_radiobutton.grid(row=2, column=0, padx=(16, 0), pady=(20, 0), sticky='nw')
        self.file_path_text.grid(row=3, column=0, padx=(16, 0), pady=(35, 0))
        self.file_path_entry.grid(row=4, column=0, padx=(16, 0), pady=(35, 0))
        self.file_path_button.grid(row=5, column=0, padx=(16, 0), pady=(35, 0))

        self.start_process_button.grid(row=6, column=0, padx=(16, 0), pady=(40, 0))
