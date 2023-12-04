import os

import customtkinter as ctk

from src.utilitybox.auxiliar.extension_operations import group_files_by_extensions
from src.utilitybox.auxiliar.file_operations import browse_folder
from src.utilitybox.auxiliar.log_functions import update_file_log
from src.utilitybox.auxiliar.operations_messages import log_basic_operation_results
from src.utilitybox.auxiliar.log_messages import path_invalid_message, update_display_log
from src.utilitybox.auxiliar.project_paths import get_project_icons_path
from src.utilitybox.functionalities.search import Search


def _perform_search(mainbox, operation_specific_identifier: str, folder_path: str, file_name: str,
                    file_extension: str = '') -> None:
    """
    Perform file search based on different criteria based on provided Params and ask the log function
    to write the results in a text file.

    Params:
        mainbox (MainBox): An instance of the MainBox class (parent).
        operation_specific_identifier (str): The operation identifier that specifies the type of operation.
        folder_path (str): The file path where the search takes place.
        file_name (str): The name of the file.
        file_extension (str): The extension of the file/files (optional).
    """
    file_extension_lower = file_extension.lower()
    operation_code = {'OK': 200, 'NO CONTENT': 204, 'BAD REQUEST': 404}

    results_id = operation_code['BAD REQUEST']
    if not os.path.exists(folder_path):
        log_message = path_invalid_message(operation_specific_identifier, results_id, folder_path)
        update_file_log(log_message, operation_specific_identifier)
        update_display_log(mainbox, operation_specific_identifier, results_id)
        return

    search = Search(folder_path)

    try:
        if not file_name:
            search.search_by_extension(file_extension_lower)
        else:
            search.search_by_name(file_name, file_extension_lower)
    except Exception as e:
        print(e)

    results_id = operation_code['OK']
    if not search.files_found:
        results_id = operation_code['NO CONTENT']

    update_display_log(mainbox, operation_specific_identifier, results_id)

    grouped_files = group_files_by_extensions(search.files_found)

    log_basic_operation_results(operation_specific_identifier, results_id, grouped_files)


class SearchWindow(ctk.CTkToplevel):
    """
    Create a window for the search functionality.

    Notes:
        The window will not close after the search is performed.
        The user can edit and modify the values as needed.
        The window must be closed manually.
    """

    def __init__(self, mainbox):
        """
        Initialize the DeleteWindow object.

        Params:
            mainbox (MainBox): An instance of the MainBox class that contains useful information
                used for different functions to keep the main window up to date.
        """
        super().__init__()
        self.title(' Search')
        self.geometry('252x385')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.operation_specific_identifier = 'Search'
        self.after(250, lambda: self.iconbitmap(
            (os.path.join(get_project_icons_path(), 'Search.ico'))))

        # Widgets implementation
        # General folder location information
        self.file_path_text = ctk.CTkLabel(master=self, text='Enter the folder path: ')
        self.file_path_entry = ctk.CTkEntry(master=self, width=220)
        self.file_path_button = ctk.CTkButton(
            master=self, text='Browse folder', font=('Helvetica', 12, 'bold'), fg_color='#00539C', text_color='white',
            command=lambda: browse_folder(self.file_path_entry))

        # File name and extension information
        self.file_name_text = ctk.CTkLabel(master=self, text='Enter the file name: ')
        self.file_name_entry = ctk.CTkEntry(master=self, width=220)
        self.file_ext_text = ctk.CTkLabel(master=self, text='Enter the file extension (optional): ')
        self.file_ext_entry = ctk.CTkEntry(master=self, width=220)

        # Action buttons
        self.start_searching_button = ctk.CTkButton(
            master=self, text='Start searching', font=('Helvetica', 12, 'bold'), fg_color='green', text_color='white',
            command=lambda: _perform_search(mainbox, self.operation_specific_identifier,
                                            self.file_path_entry.get(), self.file_name_entry.get(),
                                            self.file_ext_entry.get()))

        # Widgets placement
        self.file_path_text.grid(row=0, column=0, padx=(15, 0), pady=(15, 0))
        self.file_path_entry.grid(row=1, column=0, padx=(15, 0), pady=(15, 0))
        self.file_path_button.grid(row=2, column=0, padx=(15, 0), pady=(15, 0))
        self.file_name_text.grid(row=3, column=0, padx=(15, 0), pady=(15, 0))
        self.file_name_entry.grid(row=4, column=0, padx=(15, 0), pady=(15, 0))
        self.file_ext_text.grid(row=5, column=0, padx=(15, 0), pady=(15, 0))
        self.file_ext_entry.grid(row=6, column=0, padx=(15, 0), pady=(15, 0))

        self.start_searching_button.grid(row=7, column=0, padx=(15, 0), pady=(40, 0))
