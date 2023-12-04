import tkinter
from tkinter import filedialog
import customtkinter as ctk


def browse_folder(entry_widget: ctk.CTkEntry) -> None:
    """
    Open a file dialog to browse and select a folder.

    Params:
        entry_widget (tk.Entry): The entry widget where the selected folder path will be displayed.
    """
    folder_path = tkinter.filedialog.askdirectory()
    if folder_path:
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, folder_path)


def browse_file(entry_widget: ctk.CTkEntry) -> None:
    """
    Open a file dialog to browse and select a file.

    Params:
        entry_widget (tk.Entry): The entry widget where the selected file path will be displayed.
    """
    file_path = tkinter.filedialog.askopenfilename()
    if file_path:
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, file_path)


def browse_multiple_files() -> list[str]:
    """
    Open a file dialog to browse and select multiple files.
    """
    files = tkinter.filedialog.askopenfilenames()
    return list(files)
