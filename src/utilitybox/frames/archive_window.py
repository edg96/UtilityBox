import os
import tkinter as tk

import customtkinter as ctk

from src.utilitybox.auxiliar.file_operations import browse_file, browse_folder, browse_multiple_files
from src.utilitybox.auxiliar.log_functions import update_file_log
from src.utilitybox.auxiliar.operations_messages import log_compressing_results, log_decompressing_results
from src.utilitybox.auxiliar.log_messages import path_invalid_message, update_display_log
from src.utilitybox.auxiliar.project_paths import get_project_icons_path
from src.utilitybox.functionalities.archive import Archive

"""
File archieving Params (used for radio buttons).
"""
COMPRESS_OPTION = 1
DECOMPRESS_OPTION = 2


def _compress_files(mainbox, operation_specific_identifier: str, archive_format: str, archive_name: str,
                    file_list: list[str], file_list_basename: list[str], destination_path: str) -> None:
    """
    Compress files into an archive.

    Params:
        mainbox (MainBox): An instance of the MainBox class.
        operation_specific_identifier (str): A unique identifier for the compression operation.
        archive_format (str): The format of the archive ('zip' or 'rar').
        archive_name (str): The name of the archive.
        file_list (list[str]): List of file paths to be compressed.
        file_list_basename (list[str]): List of file basenames to be compressed.
        destination_path (str): The destination path for the archive.

    Notes:
        This function handles the compression of files into an archive.
    """
    operation_code = {'OK': 200, 'NO CONTENT': 204, 'BAD REQUEST': 404}

    all_files_valid = all(os.path.exists(file) for file in file_list)

    operation_id = operation_code['BAD REQUEST']
    if not all_files_valid:
        # Log an error message and update the display log.
        log_message = path_invalid_message(operation_specific_identifier, operation_id, destination_path)
        update_file_log(log_message, operation_specific_identifier)
        update_display_log(mainbox, operation_specific_identifier, operation_id)
        return

    archive = Archive()
    operation_id = operation_code['OK']
    try:
        if archive_format == 'rar':
            archive.compress_rar_files(archive_name, file_list_basename, destination_path)
        else:
            archive.compress_zip_files(archive_name, file_list, destination_path)
        archive.clean_files(file_list_basename, destination_path)
        update_display_log(mainbox, operation_specific_identifier, operation_id)
        log_compressing_results(operation_specific_identifier, operation_id, destination_path)
    except Exception as e:
        print(e)


def _decompress_files(mainbox, operation_specific_identifier: str, compressed_archive_location: str,
                      destination_path: str) -> None:
    """
    Decompress files from an archive.

    Params:
        mainbox (MainBox): An instance of the MainBox class.
        operation_specific_identifier (str): A unique identifier for the decompression operation.
        compressed_archive_location (str): The location of the compressed archive file.
        destination_path (str): The destination path for decompressed files.

    Notes:
        This function handles the decompression of files from an archive.
    """
    operation_code = {'OK': 200, 'BAD REQUEST': 404}
    archive = Archive()

    operation_id = operation_code['BAD REQUEST']
    if not os.path.exists(compressed_archive_location):
        log_message = path_invalid_message(operation_specific_identifier, operation_id, compressed_archive_location)
        update_file_log(log_message, operation_specific_identifier)
        update_display_log(mainbox, operation_specific_identifier, operation_id)
        return

    operation_id = operation_code['OK']
    try:
        archive_type = os.path.splitext(os.path.basename(compressed_archive_location))[1]
        if archive_type == '.rar':
            archive.decompress_rar_files(compressed_archive_location, destination_path)
        elif archive_type == '.zip':
            archive.decompress_zip_files(compressed_archive_location, destination_path)
        update_display_log(mainbox, operation_specific_identifier, operation_id)
        log_decompressing_results(operation_specific_identifier, operation_id, destination_path)
    except Exception as e:
        print(e)


def _determine_operation_type(mainbox, operation_specific_identifier: list[str], radio_button: int,
                              dropdown_current_option: str,
                              archive_name: str, file_list: list[str], compressed_archive_location: str,
                              destination_path: str, ) -> None:
    """
    Start the archiving process based on user input.

    Params:
        mainbox (MainBox): An instance of the MainBox class containing useful information.
        operation_specific_identifier (str): A unique identifier for the archive operation.
        radio_button (int): The selected radio button option (COMPRESS_OPTION or DECOMPRESS_OPTION).
        dropdown_current_option (str): The selected archive format.
        destination_path (str): The destination path for the archive or decompressed files.
        compressed_archive_location (str): The location of the compressed archive file.
        archive_name (str): The name of the archive.
        file_list (list[str]): List of selected files for the archive.
    """
    archive = Archive()
    file_list_basename = [os.path.basename(file) for file in file_list]
    if radio_button == COMPRESS_OPTION:
        archive.transfer_to_temporary_folder(file_list, destination_path)
        _compress_files(mainbox, operation_specific_identifier[0], dropdown_current_option, archive_name, file_list,
                        file_list_basename, destination_path)
    elif radio_button == DECOMPRESS_OPTION:
        _decompress_files(mainbox, operation_specific_identifier[1], compressed_archive_location, destination_path)


class ArchiveWindow(ctk.CTkToplevel):
    """
    Create a window for the archive functionality.

    Notes:
        The window will not close after the search is performed.
        The user can edit and modify the values as needed.
        The window must be closed manually.
    """

    def __init__(self, mainbox):
        """
        Initialize the ArchiveWindow object.

        Params:
            mainbox (MainBox): An instance of the MainBox class that contains useful information
                used for different functions in order to keep the main window up to date.
        """
        super().__init__()
        self.title(' Archives')
        self.geometry('252x630')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.operation_specific_identifier = ['Compress', 'Decompress']
        self.radio_current_option = 0
        self.dropdown_current_option = ''
        self.file_list = []
        self.after(250, lambda: self.iconbitmap(
            (os.path.join(get_project_icons_path(), 'Archives.ico'))))

        # Widgets functions and variables
        def radio_button_event():
            self.radio_current_option = radio_var.get()

        def archive_type_menu_callback(choice):
            self.dropdown_current_option = choice

        # The most common compression types are usually used
        archive_types = [
            'zip', 'rar'
        ]

        radio_var = tk.IntVar(value=0)

        # Widgets implementation
        # Compress
        self.encryption_radiobutton = ctk.CTkRadioButton(
            master=self, text='Compress',
            command=radio_button_event, variable=radio_var, value=1)

        self.archive_type_option_menu = ctk.StringVar(value='zip')
        self.archive_type_option_menu = ctk.CTkOptionMenu(
            master=self, values=archive_types,
            command=archive_type_menu_callback,
            variable=self.archive_type_option_menu)

        self.files_selection_button = ctk.CTkButton(
            master=self, text='Select files', font=('Helvetica', 12, 'bold'), fg_color='#00539C', text_color='white',
            command=lambda: self.update_file_list())

        # Decompress
        self.decryption_radiobutton = ctk.CTkRadioButton(
            master=self, text='Decompress',
            command=radio_button_event, variable=radio_var, value=2)

        self.archive_name_text = ctk.CTkLabel(master=self, text='Enter the archive name: ')
        self.archive_name_entry = ctk.CTkEntry(master=self, width=220)

        self.encrypted_file_path_text = ctk.CTkLabel(master=self, text='Enter the archive file path: ')
        self.encrypted_file_path_entry = ctk.CTkEntry(master=self, width=220)
        self.encrypted_file_path_button = ctk.CTkButton(
            master=self, text='Browse archive', font=('Helvetica', 12, 'bold'), fg_color='#00539C', text_color='white',
            command=lambda: browse_file(self.encrypted_file_path_entry))

        # Action buttons
        # Saving location:
        #   for compress -> location where the archive is stored
        #   for decompress -> location where the archive is decompressed
        self.saving_file_path_text = ctk.CTkLabel(master=self, text='Select the saving location: ')
        self.saving_file_path_entry = ctk.CTkEntry(master=self, width=220)
        self.saving_file_path_button = ctk.CTkButton(
            master=self, text='Save to', font=('Helvetica', 12, 'bold'), fg_color='#00539C', text_color='white',
            command=lambda: browse_folder(self.saving_file_path_entry))

        self.start_process_button = ctk.CTkButton(
            master=self, text='Start process', font=('Helvetica', 12, 'bold'), fg_color='green', text_color='white',
            command=lambda: _determine_operation_type(mainbox, self.operation_specific_identifier,
                                                      self.radio_current_option,
                                                      self.dropdown_current_option, self.archive_name_entry.get(),
                                                      self.file_list,
                                                      self.encrypted_file_path_entry.get(),
                                                      self.saving_file_path_entry.get()))

        # Widgets placement
        self.encryption_radiobutton.grid(row=1, column=0, padx=(15, 0), pady=(15, 0), sticky='nw')
        self.archive_type_option_menu.grid(row=2, column=0, padx=(15, 0), pady=(15, 0), sticky='nw')
        self.archive_name_text.grid(row=3, column=0, padx=(15, 0), pady=(15, 0), sticky='nw')
        self.archive_name_entry.grid(row=4, column=0, padx=(15, 0), pady=(15, 0), sticky='nw')
        self.files_selection_button.grid(row=5, column=0, padx=(15, 0), pady=(15, 0), sticky='nw')

        self.decryption_radiobutton.grid(row=6, column=0, padx=(15, 0), pady=(35, 0), sticky='nw')
        self.encrypted_file_path_text.grid(row=7, column=0, padx=(15, 0), pady=(15, 0), sticky='nw')
        self.encrypted_file_path_entry.grid(row=8, column=0, padx=(15, 0), pady=(15, 0), sticky='nw')
        self.encrypted_file_path_button.grid(row=9, column=0, padx=(15, 0), pady=(15, 0))

        self.saving_file_path_text.grid(row=10, column=0, padx=(15, 0), pady=(35, 0))
        self.saving_file_path_entry.grid(row=11, column=0, padx=(15, 0), pady=(15, 0))
        self.saving_file_path_button.grid(row=12, column=0, padx=(15, 0), pady=(15, 0))

        self.start_process_button.grid(row=13, column=0, padx=(15, 0), pady=(40, 0))

    def update_file_list(self) -> None:
        """
        Updates the internal list of files attributed to the ArchiveWindow object.
        """
        selected_files = browse_multiple_files().copy()
        if selected_files:
            self.file_list = selected_files
