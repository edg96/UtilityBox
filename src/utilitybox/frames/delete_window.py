import os
import tkinter as tk

import customtkinter as ctk

from auxiliar import log_functions, reusable_functions
from functionalities.delete import Delete
from auxiliar.path_validator import check_path_existence

"""
File deletion parameters (used for radio buttons).
"""
DELETE_SINGLE_EXTENSION = 1
DELETE_MULTIPLE_EXTENSIONS = 2
DELETE_BY_KEYWORD = 3


def _log_sigle_multiple_extension_keyword_results(operation_specific_identifier: str, operation_id: int, files_deleted: dict[str, list[str]]) -> None:
    """
    Log the results of sorting files by single or multiple extensions.

    Parameters:
        operation_specific_identifier (str): The identifier for the sorting operation.
        operation_id (int): The operation's status code (200 for success, 204 for no content, 404 for error).
        files_deleted (dict[str, list[str]]): A dictionary containing deleted files grouped by extension.
    """
    # Construct a log message with deletion results and update the file log.
    log_file_message = (f'[{operation_specific_identifier.upper()}: {operation_id}]:'
                        f'\nDeleted the following files:')

    if files_deleted:
        for extension in files_deleted:
            log_file_message = log_file_message + f'\n\tFiles of type: {extension}'
            for index, file in enumerate(files_deleted[extension], start=1):
                log_file_message = log_file_message + f'\n\t\t{file}'

    log_functions.update_file_log(log_file_message, operation_specific_identifier)


def _log_no_results(operation_specific_identifier: str, operation_id: int) -> None:
    """
    Log when no files were deleted in a deletion operation.

    Parameters:
        operation_specific_identifier (str): The identifier for the deletion operation.
        operation_id (int): The operation's status code (200 for success, 204 for no content, 404 for error).
    """
    # Construct a log message indicating no files were deleted and update the file log.
    log_file_message = (f'[{operation_specific_identifier.upper()}: {operation_id}]:'
                        f'\nDeleted the following files:'
                        f'\n\tNone')

    log_functions.update_file_log(log_file_message, operation_specific_identifier)


def _delete_files(mainbox, operation_specific_identifier: str, radio_option: int,
                  folder_path: str, file_extension: str, list_of_file_extensions: str,
                  keyword: str, keyword_extension: str) -> None:
    """
    Perform file deletion based on different criteria based on provided parameters and log the results.

    Parameters:
        mainbox (MainBox): An instance of the MainBox class (parent).
        operation_specific_identifier (str): The identifier for the deletion operation.
        radio_option (int): The selected radio button option for deletion (1, 2, or 3).
        folder_path (str): The file path where the deletion takes place.
        file_extension (str): The extension of the file to delete (for single extension deletion).
        list_of_file_extensions (str): A comma-separated list of extensions (for multiple extensions deletion).
        keyword (str): The keyword for file deletion (for deletion by keyword).
        keyword_extension (str): The file extension for keyword-based deletion (for deletion by keyword).
    """
    operation_code = {'OK': 200, 'NO CONTENT': 204, 'BAD REQUEST': 404}

    operation_id = operation_code['BAD REQUEST']
    if not check_path_existence(folder_path):
        log_message = reusable_functions.path_invalid_message(operation_specific_identifier, operation_id, folder_path)
        log_functions.update_file_log(log_message, operation_specific_identifier)
        reusable_functions.update_display_log(mainbox, operation_specific_identifier, operation_id)
        return

    delete = Delete(folder_path)
    try:
        if radio_option == DELETE_SINGLE_EXTENSION:
            delete.delete_by_single_extension(file_extension)
        elif radio_option == DELETE_MULTIPLE_EXTENSIONS:
            delete.delete_by_multiple_extensions(list_of_file_extensions)
        elif radio_option == DELETE_BY_KEYWORD:
            delete.delete_by_keyword(keyword, keyword_extension)
    except Exception as e:
        print(e)

    operation_id = operation_code['OK']
    if not delete.deleted_files and not delete.deleted_files_by_extension:
        operation_id = operation_code['NO CONTENT']

    reusable_functions.update_display_log(mainbox, operation_specific_identifier, operation_id)

    # Log sorting results based on the selected sorting option.
    if delete.deleted_files or delete.deleted_files_by_extension:
        _log_sigle_multiple_extension_keyword_results(operation_specific_identifier, operation_id, delete.deleted_files)
    else:
        _log_no_results(operation_specific_identifier, operation_id)


class DeleteWindow(ctk.CTkToplevel):
    def __init__(self, mainbox):
        """
        Create a window for the delete functionality.

        Parameters:
            mainbox (MainBox): An instance of the MainBox class that contain usefull information
                used for different functions in order to keep the main window up to date.

        Notes:
            The window will not close after the search is performed.
            The user can edit and modify the values as needed.
            The window must be closed manually.
        """
        super().__init__()
        self.title(' Delete')
        self.geometry('252x695')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.operation_specific_identifier = 'Delete'
        self.radio_current_option = 0
        self.dropdown_current_option = ''
        self.after(250, lambda: self.iconbitmap(
            (os.path.join(reusable_functions.get_project_icons_path(), 'Delete.ico'))))

        # Widgets functions and variables
        def radiobutton_event():
            self.radio_current_option = radio_var.get()

        def option_menu_extensions_callback(choice):
            self.dropdown_current_option = choice

        # The most common extension that are usually found in a system
        common_file_extensions = [
            'txt', 'doc', 'docx', 'pdf', 'xlsx', 'ppt', 'jpg', 'jpeg', 'png', 'gif',
            'mp3', 'mp4', 'avi', 'mov', 'html', 'css', 'js', 'json', 'xml', 'csv',
            'zip', 'rar', 'tar', 'gz', 'exe', 'dll', 'py', 'java', 'cpp', 'php',
            'rb', 'html', 'sql', 'md'
        ]

        # Widgets implementation
        # General folder location information
        self.folder_path_text = ctk.CTkLabel(master=self, text='Enter the folder path: ')
        self.folder_path_entry = ctk.CTkEntry(master=self, width=220)
        self.folder_path_button = ctk.CTkButton(
            master=self, text='Browse folder', font=('Helvetica', 12, 'bold'), fg_color='#00539C', text_color='white',
            command=lambda: reusable_functions.browse_folder(self.folder_path_entry))

        # Single extension deleting
        radio_var = tk.IntVar(value=0)
        self.delete_by_specific_extension_radiobutton = ctk.CTkRadioButton(
            master=self, text='Delete by single extension',
            command=radiobutton_event, variable=radio_var, value=1)
        self.option_menu_extensions = ctk.StringVar(value='All extension')
        self.option_menu_extensions = ctk.CTkOptionMenu(
            master=self, values=common_file_extensions,
            command=option_menu_extensions_callback,
            variable=self.option_menu_extensions)

        # Multiple extensions deleting
        self.delete_by_multiple_extensions_radiobutton = (ctk.CTkRadioButton(
            master=self, text='Delete by multiple extensions',
            command=radiobutton_event, variable=radio_var, value=2))
        self.delete_by_multiple_extensions_text = ctk.CTkLabel(
            master=self, text='Enter all the extensions separated \nby commas:\t\t        ')
        self.delete_by_multiple_extension_entry = ctk.CTkEntry(
            master=self, width=220)

        # Keyword deleting
        self.delete_by_keyword_button = ctk.CTkRadioButton(
            master=self, text='Keyword deleting:',
            command=radiobutton_event, variable=radio_var, value=3)
        self.delete_by_keyword_text = ctk.CTkLabel(master=self, text='Enter the keyword: ')
        self.delete_by_keyword_entry = ctk.CTkEntry(master=self, width=220)
        self.delete_by_keyword_extension_text = ctk.CTkLabel(master=self, text='Enter the keyword: ')
        self.delete_by_keyword_extension_entry = ctk.CTkEntry(master=self, width=220)

        # Action buttons
        self.start_deleting_button = ctk.CTkButton(
            master=self, text='Start deleting', font=('Helvetica', 12, 'bold'), fg_color='green', text_color='white',
            command=lambda: _delete_files(mainbox, self.operation_specific_identifier, self.radio_current_option,
                                          self.folder_path_entry.get(), self.dropdown_current_option,
                                          self.delete_by_multiple_extension_entry.get(),
                                          self.delete_by_keyword_entry.get(), self.delete_by_keyword_extension_entry.get()))

        # Widgets placement
        self.folder_path_text.grid(row=0, column=0, padx=(15, 0), pady=(15, 0))
        self.folder_path_entry.grid(row=1, column=0, padx=(15, 0), pady=(15, 0))
        self.folder_path_button.grid(row=2, column=0, padx=(15, 0), pady=(15, 0))

        self.delete_by_specific_extension_radiobutton.grid(row=3, column=0, padx=(15, 0), pady=(35, 0), sticky='nw')
        self.option_menu_extensions.grid(row=4, column=0, padx=(15, 0), pady=(15, 0), sticky='nw')

        self.delete_by_multiple_extensions_radiobutton.grid(row=5, column=0, padx=(15, 0), pady=(35, 0), sticky='nw')
        self.delete_by_multiple_extensions_text.grid(row=6, column=0, padx=(20, 0), pady=(15, 0), sticky='nw')
        self.delete_by_multiple_extension_entry.grid(row=7, column=0, padx=(15, 0), pady=(15, 0))

        self.delete_by_keyword_button.grid(row=8, column=0, padx=(15, 0), pady=(35, 0), sticky='nw')
        self.delete_by_keyword_text.grid(row=9, column=0, padx=(20, 0), pady=(15, 0), sticky='nw')
        self.delete_by_keyword_entry.grid(row=10, column=0, padx=(15, 0), pady=(15, 0))
        self.delete_by_keyword_extension_text.grid(row=11, column=0, padx=(20, 0), pady=(15, 0), sticky='nw')
        self.delete_by_keyword_extension_entry.grid(row=12, column=0, padx=(15, 0), pady=(15, 0))

        self.start_deleting_button.grid(row=13, column=0, padx=(15, 0), pady=(40, 0))
