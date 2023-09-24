import os

import customtkinter as ctk

from src.utilitybox.auxiliar import log_functions, reusable_functions
from src.utilitybox.auxiliar.path_validator import check_path_existence
from src.utilitybox.functionalities.search import Search


def _build_message_and_log(operation_specific_identifier: str, operation_id: int, files_found: list[str]) -> None:
    """
    Iterate through a list of files found in the searching process and construct a detailed result
    that will be passed as a message in order for it to be logged in a file.

    Parameters:
        operation_specific_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): The numbers of files found after the searching.
        files_found (list[str]): A list of file names found during the search.
    """
    log_file_message = (f'[{operation_specific_identifier.upper()}: {operation_id}]:'
                        f'\nFound the following results:\n')
    if files_found:
        for index, file in enumerate(files_found, start=1):
            if index != len(files_found):
                log_file_message = log_file_message + f'\t{file}\n'
            else:
                log_file_message = log_file_message + f'\t{file}'
    else:
        log_file_message = log_file_message + '\tNone'

    log_functions.update_file_log(log_file_message, operation_specific_identifier)


def _determine_search_type(mainbox, operation_specific_identifier: str,
                           folder_path: str, file_name: str, file_extension: str = '') -> None:
    """
    Perform file search based on different criteria based on provided parameters and log the results.

    Creates an instance of Path Validator that is responsible for checking the file path validity.
    If the check passes then the searching takes place (the type of search is distributed depending
    on the parameters provided).
    The information is logged to a file and to the log frame, both serving a different purpose:
    - file: used for creating a history detailed information based on the events generated
    by the user
    - log box: used for user interaction (informing the user about the results of the events)

    Parameters:
        mainbox (MainBox): An instance of the MainBox class (parent).
        operation_specific_identifier (str): The operation identifier that specifies the type of operation.
        folder_path (str): The file path where the search takes place.
        file_name (str): The name of the file.
        file_extension (str): The extension of the file/files (optional).
    """
    file_extension_lower = file_extension.lower()
    operation_code = {'OK': 200, 'NO CONTENT': 204, 'BAD REQUEST': 404}

    operation_id = operation_code['BAD REQUEST']
    if not check_path_existence(folder_path):
        log_message = reusable_functions.path_invalid_message(operation_specific_identifier, operation_id, folder_path)
        log_functions.update_file_log(log_message, operation_specific_identifier)
        reusable_functions.update_display_log(mainbox, operation_specific_identifier, operation_id)
        return

    search = Search(folder_path)
    try:
        if file_name and not file_extension_lower:
            search.search_by_name(file_name, file_extension_lower)
        else:
            search.search_by_extension(file_extension_lower)
    except Exception as e:
        print(e)

    operation_id = operation_code['OK']
    if not search.file_list_by_name and not search.file_list_by_ext:
        operation_id = operation_code['NO CONTENT']

    reusable_functions.update_display_log(mainbox, operation_specific_identifier, operation_id)

    if search.file_list_by_name:
        _build_message_and_log(operation_specific_identifier, operation_id, search.file_list_by_name)
    elif search.file_list_by_ext:
        _build_message_and_log(operation_specific_identifier, operation_id, search.file_list_by_ext)


class SearchWindow(ctk.CTkToplevel):
    def __init__(self, mainbox):
        """
        Create a window for the search functionality.

        Parameters:
            mainbox (MainBox): An instance of the MainBox class that contain usefull information
                used for different functions in order to keep the main window up to date.

        Notes:
            The window will not close after the search is performed.
            The user can edit and modify the values as needed.
            The window must be closed manually.
        """
        super().__init__()
        self.title(' Search')
        self.geometry('252x385')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.operation_specific_identifier = 'Search'
        self.after(250, lambda: self.iconbitmap(
            (os.path.join(reusable_functions.get_project_icons_path(), 'Search.ico'))))

        # Widgets implementation
        # General folder location information
        self.file_path_text = ctk.CTkLabel(master=self, text='Enter the folder path: ')
        self.file_path_entry = ctk.CTkEntry(master=self, width=220)
        self.file_path_button = ctk.CTkButton(
            master=self, text='Browse folder', font=('Helvetica', 12, 'bold'), fg_color='#00539C', text_color='white',
            command=lambda: reusable_functions.browse_folder(self.file_path_entry))

        # File name and extension information
        self.file_name_text = ctk.CTkLabel(master=self, text='Enter the file name: ')
        self.file_name_entry = ctk.CTkEntry(master=self, width=220)
        self.file_ext_text = ctk.CTkLabel(master=self, text='Enter the file extension (optional): ')
        self.file_ext_entry = ctk.CTkEntry(master=self, width=220)

        # Action buttons
        self.start_searching_button = ctk.CTkButton(
            master=self, text='Start searching', font=('Helvetica', 12, 'bold'), fg_color='green', text_color='white',
            command=lambda: _determine_search_type(mainbox, self.operation_specific_identifier,
                                                   self.file_path_entry.get(), self.file_name_entry.get(), self.file_ext_entry.get()))

        # Widgets placement
        self.file_path_text.grid(row=0, column=0, padx=(15, 0), pady=(15, 0))
        self.file_path_entry.grid(row=1, column=0, padx=(15, 0), pady=(15, 0))
        self.file_path_button.grid(row=2, column=0, padx=(15, 0), pady=(15, 0))
        self.file_name_text.grid(row=3, column=0, padx=(15, 0), pady=(15, 0))
        self.file_name_entry.grid(row=4, column=0, padx=(15, 0), pady=(15, 0))
        self.file_ext_text.grid(row=5, column=0, padx=(15, 0), pady=(15, 0))
        self.file_ext_entry.grid(row=6, column=0, padx=(15, 0), pady=(15, 0))

        self.start_searching_button.grid(row=7, column=0, padx=(15, 0), pady=(40, 0))
