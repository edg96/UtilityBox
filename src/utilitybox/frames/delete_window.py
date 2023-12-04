import os
import tkinter as tk

import customtkinter as ctk

from src.utilitybox.auxiliar.extension_operations import group_files_by_extensions
from src.utilitybox.auxiliar.file_operations import browse_folder
from src.utilitybox.auxiliar.log_functions import update_file_log
from src.utilitybox.auxiliar.operations_messages import log_basic_operation_results
from src.utilitybox.auxiliar.log_messages import path_invalid_message, update_display_log
from src.utilitybox.auxiliar.project_paths import get_project_icons_path
from src.utilitybox.functionalities.delete import Delete

"""
File deletion Params (used for radio buttons).
"""
DELETE_SINGLE_EXTENSION = 1
DELETE_MULTIPLE_EXTENSIONS = 2
DELETE_BY_KEYWORD = 3


def _perform_deletion(mainbox, operation_specific_identifier: str, radio_option: int,
                      folder_path: str, file_extension: str, list_of_file_extensions: str,
                      keyword: str, keyword_extension: str) -> None:
    """
    Perform file deletion based on different criteria based on provided Params and log the results.

    Params:
        mainbox (MainBox): An instance of the MainBox class (parent).
        operation_specific_identifier (str): The identifier for the deletion operation.
        radio_option (int): The selected radio button option for deletion (1, 2, or 3).
        folder_path (str): The file path where the deletion takes place.
        file_extension (str): The extension of the file to delete (for single extension deletion).
        list_of_file_extensions (str): A comma-separated list of extensions (for multiple extensions deletion).
        keyword (str): The keyword for file deletion (for deletion by keyword).
        keyword_extension (str): The file extension for keyword-based deletion (for deletion by keyword).
    """
    file_extension_lower = file_extension.lower()
    operation_code = {'OK': 200, 'NO CONTENT': 204, 'BAD REQUEST': 404}

    results_id = operation_code['BAD REQUEST']
    if not os.path.exists(folder_path):
        log_message = path_invalid_message(operation_specific_identifier, results_id, folder_path)
        update_file_log(log_message, operation_specific_identifier)
        update_display_log(mainbox, operation_specific_identifier, results_id)
        return

    delete = Delete(folder_path)

    try:
        if radio_option == DELETE_SINGLE_EXTENSION:
            delete.delete_by_single_extension(file_extension_lower)
        elif radio_option == DELETE_MULTIPLE_EXTENSIONS:
            delete.delete_by_multiple_extensions(list_of_file_extensions)
        elif radio_option == DELETE_BY_KEYWORD:
            delete.delete_by_keyword(keyword, keyword_extension)
    except Exception as e:
        print(e)

    results_id = operation_code['OK']
    if not delete.files_deleted:
        results_id = operation_code['NO CONTENT']

    update_display_log(mainbox, operation_specific_identifier, results_id)

    grouped_files = group_files_by_extensions(delete.files_deleted)

    log_basic_operation_results(operation_specific_identifier, results_id, grouped_files)


class DeleteWindow(ctk.CTkToplevel):
    """
    Create a window for the delete functionality.

    Notes:
        The window will not close after the search is performed.
        The user can edit and modify the values as needed.
        The window must be closed manually.
    """

    def __init__(self, mainbox):
        """
        Initialize the DeleteWindow object.

        Params:
            mainbox (MainBox): An instance of the MainBox class that contain usefully information
                used for different functions in order to keep the main window up to date.
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
            (os.path.join(get_project_icons_path(), 'Delete.ico'))))

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
            command=lambda: browse_folder(self.folder_path_entry))

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
        self.delete_by_keyword_extension_text = ctk.CTkLabel(master=self, text='Enter the extension: ')
        self.delete_by_keyword_extension_entry = ctk.CTkEntry(master=self, width=220)

        # Action buttons
        self.start_deleting_button = ctk.CTkButton(
            master=self, text='Start deleting', font=('Helvetica', 12, 'bold'), fg_color='green', text_color='white',
            command=lambda: _perform_deletion(mainbox, self.operation_specific_identifier, self.radio_current_option,
                                              self.folder_path_entry.get(), self.dropdown_current_option,
                                              self.delete_by_multiple_extension_entry.get(),
                                              self.delete_by_keyword_entry.get(),
                                              self.delete_by_keyword_extension_entry.get()))

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
