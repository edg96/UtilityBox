import os
import tkinter as tk

import customtkinter as ctk

from src.utilitybox.auxiliar.extension_operations import group_files_by_extensions
from src.utilitybox.auxiliar.file_operations import browse_folder
from src.utilitybox.auxiliar.log_functions import update_file_log
from src.utilitybox.auxiliar.operations_messages import log_basic_operation_results
from src.utilitybox.auxiliar.log_messages import path_invalid_message, update_display_log
from src.utilitybox.auxiliar.project_paths import get_project_icons_path
from src.utilitybox.functionalities.sort import Sort

"""
File sorting Params (used for radio buttons).
"""
SORT_SINGLE_EXTENSION = 1
SORT_MULTIPLE_EXTENSIONS = 2
SORT_BY_KEYWORD = 3


def _perform_sort(mainbox, operation_specific_identifier: str, radio_option: int,
                  folder_path: str, file_extension: str, list_of_file_extensions: str,
                  keyword: str, keyword_extension: str, new_name: str) -> None:
    """
    Determine the type of sorting operation and perform the sorting based on user inputs.

    Params:
        mainbox: An instance of the MainBox class for updating the main window.
        operation_specific_identifier (str): The identifier for the sorting operation.
        radio_option (int): The selected radio button option for sorting.
        folder_path (str): The folder path to perform sorting within.
        list_of_file_extensions: A list of file extensions for multiple extension sorting.
        file_extension: The selected file extension for single extension sorting.
        keyword (str): The keyword used for keyword-based sorting.
        keyword_extension (str): The extension used for keyword-based sorting.
        new_name: The new name for files in keyword-based sorting.

    Notes:
        This function performs file sorting and logs the results.
    """
    file_extension_lower = file_extension.lower()
    operation_code = {'OK': 200, 'NO CONTENT': 204, 'BAD REQUEST': 404}

    results_id = operation_code['BAD REQUEST']
    if not os.path.exists(folder_path):
        log_message = path_invalid_message(operation_specific_identifier, results_id, folder_path)
        update_file_log(log_message, operation_specific_identifier)
        update_display_log(mainbox, operation_specific_identifier, results_id)
        return

    sort = Sort(folder_path)

    try:
        if radio_option == SORT_SINGLE_EXTENSION:
            sort.index_single_extension(file_extension_lower)
        elif radio_option == SORT_MULTIPLE_EXTENSIONS:
            sort.index_multiple_extensions(list_of_file_extensions)
        else:
            sort.sort_and_index_by_keyword(keyword, keyword_extension, new_name)
    except Exception as e:
        print(e)

    results_id = operation_code['OK']
    if not sort.files_moved:
        results_id = operation_code['NO CONTENT']

    update_display_log(mainbox, operation_specific_identifier, results_id)

    grouped_files = group_files_by_extensions(sort.files_moved)

    log_basic_operation_results(operation_specific_identifier, results_id, grouped_files)


class SortWindow(ctk.CTkToplevel):
    """
    Create a window for the sort functionality.

    Notes:
        The window will not close after the search is performed.
        The user can edit and modify the values as needed.
        The window must be closed manually.
    """

    def __init__(self, mainbox):
        """
        Initialize the SortWindow object.

        Params:
            mainbox (MainBox): An instance of the MainBox class that contains useful information
                used for different functions to keep the main window up to date.
        """
        super().__init__()
        self.title(' Sort')
        self.geometry('252x780')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.operation_unique_identifier = 'Sort'
        self.radio_current_option = 0
        self.dropdown_current_option = ''
        self.after(250, lambda: self.iconbitmap(
            (os.path.join(get_project_icons_path(), 'Sort.ico'))))

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

        # Single extension sorting
        radio_var = tk.IntVar(value=0)
        self.sort_by_specific_extension_radiobutton = ctk.CTkRadioButton(
            master=self, text='Sort by single extension',
            command=radiobutton_event, variable=radio_var, value=1)
        self.option_menu_extensions = ctk.StringVar(value='Select extension')
        self.option_menu_extensions = ctk.CTkOptionMenu(
            master=self, values=common_file_extensions,
            command=option_menu_extensions_callback,
            variable=self.option_menu_extensions)

        # Multiple extensions sorting
        self.sort_by_multiple_extensions_radiobutton = ctk.CTkRadioButton(
            master=self, text='Sort by multiple extensions',
            command=radiobutton_event, variable=radio_var, value=2)
        self.sort_by_multiple_extensions_text = ctk.CTkLabel(master=self,
                                                             text='Enter all the extensions separated \nby commas:\t\t        ')
        self.sort_by_multiple_extension_entry = ctk.CTkEntry(master=self, width=220)

        # Keyword sorting
        self.sort_by_keyword_button = ctk.CTkRadioButton(
            master=self, text='Keyword sorting:',
            command=radiobutton_event, variable=radio_var, value=3)
        self.sort_by_keyword_text = ctk.CTkLabel(master=self, text='Enter the keyword: ')
        self.sort_by_keyword_entry = ctk.CTkEntry(master=self, width=220)
        self.sort_by_keyword_extension_text = ctk.CTkLabel(master=self, text='Enter the extension: ')
        self.sort_by_keyword_extension_entry = ctk.CTkEntry(master=self, width=220)
        self.sort_by_keyword_new_name_text = ctk.CTkLabel(master=self, text='Enter the new name: ')
        self.sort_by_keyword_new_name_entry = ctk.CTkEntry(master=self, width=220)

        # Action buttons
        self.start_sorting_button = ctk.CTkButton(
            master=self, text='Start sorting', font=('Helvetica', 12, 'bold'), fg_color='green', text_color='white',
            command=lambda: _perform_sort(mainbox, self.operation_unique_identifier, self.radio_current_option,
                                          self.folder_path_entry.get(), self.dropdown_current_option,
                                          self.sort_by_multiple_extension_entry.get(), self.sort_by_keyword_entry.get(),
                                          self.sort_by_keyword_extension_entry.get(),
                                          self.sort_by_keyword_new_name_entry.get()))

        # Widgets placement
        self.folder_path_text.grid(row=0, column=0, padx=(15, 0), pady=(15, 0))
        self.folder_path_entry.grid(row=1, column=0, padx=(15, 0), pady=(15, 0))
        self.folder_path_button.grid(row=2, column=0, padx=(15, 0), pady=(15, 0))

        self.sort_by_specific_extension_radiobutton.grid(row=3, column=0, padx=(15, 0), pady=(35, 0), sticky='nw')
        self.option_menu_extensions.grid(row=4, column=0, padx=(15, 0), pady=(15, 0), sticky='nw')

        self.sort_by_multiple_extensions_radiobutton.grid(row=5, column=0, padx=(15, 0), pady=(35, 0), sticky='nw')
        self.sort_by_multiple_extensions_text.grid(row=6, column=0, padx=(20, 0), pady=(15, 0), sticky='nw')
        self.sort_by_multiple_extension_entry.grid(row=7, column=0, padx=(15, 0), pady=(15, 0))

        self.sort_by_keyword_button.grid(row=8, column=0, padx=(15, 0), pady=(35, 0), sticky='nw')
        self.sort_by_keyword_text.grid(row=9, column=0, padx=(20, 0), pady=(15, 0), sticky='nw')
        self.sort_by_keyword_entry.grid(row=10, column=0, padx=(15, 0), pady=(15, 0))
        self.sort_by_keyword_extension_text.grid(row=11, column=0, padx=(20, 0), pady=(15, 0), sticky='nw')
        self.sort_by_keyword_extension_entry.grid(row=12, column=0, padx=(15, 0), pady=(15, 0))
        self.sort_by_keyword_new_name_text.grid(row=13, column=0, padx=(20, 0), pady=(15, 0), sticky='nw')
        self.sort_by_keyword_new_name_entry.grid(row=14, column=0, padx=(15, 0), pady=(15, 0))

        self.start_sorting_button.grid(row=15, column=0, padx=(15, 0), pady=(40, 0))
