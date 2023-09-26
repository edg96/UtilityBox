import os.path
import shutil

from src.utilitybox.auxiliar import reusable_functions


class Sort:
    """
    Utility class for sorting files of a certain type by specific criteria.

    Parameters:
        folder_path (str): The folder path where the sorting takes place.

    Attributes:
        files_per_extension (dict[str, list[str]]): A dictionary containing the files (value)
            associated which each extension (key) that was sorted in the process.
        files_by_single_extension (list[str]): A list of files sorted by a single extension.
        files_by_keyword (dict[str, str]): A dictionary containing the old file name (value)
            and it's new name (key) that resulted after the sorting process.
    """
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.files_per_extension = {}
        self.files_by_single_extension = []
        self.files_by_keyword = {}

    def check_folder_existence(self, folder_name: str) -> None:
        """
        Checks if a folder with a specific name exists.
        Creates it if it doesn't exist.

        Parameters:
            folder_name (str): The name of the folder.
        """
        searched_folder = os.path.join(self.folder_path, folder_name)
        if not os.path.exists(searched_folder):
            os.mkdir(searched_folder)

    def indexing_single_extension(self, file_extension: str) -> None:
        """
        Indexes a single type of files by a specific extension.
        Creates folders as needed.

        Parameters:
            file_extension (str): The file extension for sorting.
        """
        files = os.listdir(self.folder_path)

        for file in files:
            _, current_file_extension = os.path.splitext(file)
            if file.endswith(file_extension) and current_file_extension:
                current_file_path = os.path.join(self.folder_path, file)
                if file_extension not in self.files_per_extension:
                    self.files_per_extension[file_extension] = []
                self.files_per_extension[file_extension].append(file)
                shutil.move(current_file_path, os.path.join(self.folder_path, file_extension))

    def indexing_multiple_extensions(self, file_extensions: str) -> None:
        """
        Sorts multiple types of files by a set of specific extensions.
        Creates folders as needed.

        Parameters:
            file_extensions (list[str]): A string of file extensions.
        """
        list_of_file_extensions = reusable_functions.split_extensions(file_extensions)
        for extension in list_of_file_extensions:
            self.check_folder_existence(extension)
            self.indexing_single_extension(extension)
            self.files_by_single_extension.clear()

    def sort_and_index_by_keyword(self, name_keyword: str, file_extension: str, new_name: str):
        """
        Sorts and indexes a set of files using a specific extension provided by the user.
        Renames files based on the provided name keyword and their order in the folder.

        Parameters:
            name_keyword (str): The keyword to identify files to be renamed.
            file_extension (str): The file extension for filtering and renaming.
            new_name (str): The new base name for the renamed files.

        Notes:
            The function scans the files in the specified folder and performs the following actions:
                - Identifies the files with names containing the specified 'name_keyword' and having
                    the given 'file_extension.'
                - Renames these files (completly erasing the old name) with the name_keyword and append
                    an index to it.
                - Moves the renamed files to a subfolder with the 'new_name' as its name.
        """
        files = os.listdir(self.folder_path)
        destination_folder = os.path.join(self.folder_path, new_name)

        self.check_folder_existence(destination_folder)

        file_index = 1
        for file in files:
            current_file_name, current_file_extension = os.path.splitext(file)
            if name_keyword in current_file_name and file.endswith(file_extension):
                new_file_name = f"{new_name}_{file_index}{current_file_extension}"
                old_path = os.path.join(self.folder_path, file)
                new_path = os.path.join(self.folder_path, new_name, new_file_name)
                self.files_by_keyword[file] = new_file_name
                os.rename(old_path, new_path)
                file_index += 1
