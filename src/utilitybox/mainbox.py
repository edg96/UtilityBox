import os.path

import customtkinter as ctk

from auxiliar import reusable_functions
from auxiliar.configure_log import LogConfigurer

__author__ = 'Dragos-Gabriel Enache'
__copyright__ = 'N/A'
__credits__ = ['N/A']

__license__ = 'N/A'
__version__ = "1.0.1"
__maintainer__ = 'Dragos-Gabriel Enache'
__email__ = 'edragosgabriel@gmail.com'
__status__ = 'Development'


__all__ = []


"""
================== Application description and main parent ==================

This module contains the main class of the problem - Mainbox
Mainbox contains the root of the tkinter application.
Has the following roles:
    - design oriented (implements the main frames - functionalities and logs)
    - operational (contains the buttons with the functionalities available through the application)
    - informational (contains the logs details - communicate with the user if the operation was 
        either successful or resulted in a failure and explains the reason)
    - organizational (check for the logging folders hierarchy):
        Parent => Year
            Child 1 => Month
                Child 1 to N => Functionalities (Search, Rename, Compare) etc

Important note: Mainbox should only contain the simple interface. It must be simply and intuitive.
      All the outer operations should be placed in special designated .py files that are
        specific and concise in their names and functionalities.
"""


class MainBox(ctk.CTk):
    def __init__(self):
        # Main windows specifications
        super().__init__()
        self.button_click = None
        self.title(' Utility Box')
        self.geometry('850x430')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.window_already_open = False
        self.toplevel_window = None
        self.numberentries = 0
        self.after(250, lambda: self.iconbitmap(
            os.path.join(reusable_functions.get_project_icons_path(), 'Main.ico')))

        self.operation_frame = ctk.CTkFrame(master=self, width=172, height=400, corner_radius=20,
                                            border_width=1, border_color='#474B4F')
        self.operation_frame.grid_propagate(False)
        self.operation_frame.grid(row=0, column=1, padx=15, pady=(13, 0))

        self.search_button = ctk.CTkButton(self.operation_frame, text='Search', font=('Helvetica', 12, 'bold'),
                                           fg_color='#00539C', text_color='white',
                                           command=lambda: self.create_search_window())
        self.search_button.grid(row=0, column=0, padx=15, pady=(13, 0))

        self.sort_button = ctk.CTkButton(self.operation_frame, text='Sort', font=('Helvetica', 12, 'bold'),
                                         fg_color='#00539C', text_color='white',
                                         command=lambda: self.create_sort_window())
        self.sort_button.grid(row=1, column=0, padx=0, pady=(15, 0))

        self.delete_button = ctk.CTkButton(self.operation_frame, text='Delete', font=('Helvetica', 12, 'bold'),
                                           fg_color='#00539C', text_color='white',
                                           command=lambda: self.create_delete_window())
        self.delete_button.grid(row=2, column=0, padx=0, pady=(15, 0))

        self.encryption_button = ctk.CTkButton(self.operation_frame, text='Data Protection',
                                               font=('Helvetica', 12, 'bold'), fg_color='#00539C', text_color='white',
                                               command=lambda: self.create_data_protection_window())
        self.encryption_button.grid(row=3, column=0, padx=0, pady=(15, 0))

        self.preview_button = ctk.CTkButton(self.operation_frame, text='Archives', font=('Helvetica', 12, 'bold'),
                                            fg_color='#00539C', text_color='white',
                                            command=lambda: self.create_archive_window())
        self.preview_button.grid(row=4, column=0, pady=(15, 0))

        self.clear_log_button = ctk.CTkButton(self.operation_frame, text='Clear log', font=('Helvetica', 12, 'bold'),
                                              fg_color='#00539C', text_color='white',
                                              command=self.button_click)
        self.clear_log_button.grid(row=8, column=0, pady=(145, 0))

        self.log_frame = ctk.CTkScrollableFrame(master=self, width=580, height=360, corner_radius=20,
                                                border_width=1, border_color='#474B4F')
        self.log_frame.grid(row=0, column=2, padx=15, pady=(13, 0))

    # Create each window from
    def create_search_window(self):
        from frames.search_window import SearchWindow
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SearchWindow(self)
        else:
            self.toplevel_window.focus()

    def create_sort_window(self):
        from frames.sort_window import SortWindow
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SortWindow(self)
        else:
            self.toplevel_window.focus()

    def create_delete_window(self):
        from frames.delete_window import DeleteWindow
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DeleteWindow(self)
        else:
            self.toplevel_window.focus()

    def create_data_protection_window(self):
        from frames.data_protection_window import DataProtectionWindow
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DataProtectionWindow(self)
        else:
            self.toplevel_window.focus()

    def create_archive_window(self):
        from frames.archive_window import ArchiveWindow
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ArchiveWindow(self)
        else:
            self.toplevel_window.focus()

    def update_log(self, log_message: str, specific_operation_color: str) -> None:
        """
        Updates the logging frame box with the message given.

        Parameters:
            log_message (str): The log message to be displayed.
            specific_operation_color (str): The color for displaying the log message.

        Returns:
            None
        """
        log_text = ctk.CTkTextbox(master=self.log_frame, width=565, height=20, corner_radius=20,
                                  fg_color=specific_operation_color,
                                  font=('Helvetica', 14, 'bold'))
        log_text.grid(row=self.numberentries, column=0, pady=(0, 10), sticky='w')
        log_text.insert(ctk.END, log_message)
        self.numberentries += 1


def check_log_folders() -> None:
    """
    Create logging folders if they do not exist.

    This function initializes the Log Configurer and checks for the year, month, and category folders.
    If any of these folders are missing, it creates them.

    Returns:
        None
    """
    log_configurer = LogConfigurer()
    log_configurer.check_and_create_year_folder()
    log_configurer.check_and_create_month_folder()
    log_configurer.create_category()


if __name__ == '__main__':
    mainbox = MainBox()
    mainbox.mainloop()
