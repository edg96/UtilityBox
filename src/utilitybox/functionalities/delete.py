import os.path

from src.utilitybox.auxiliar import reusable_functions


class Delete:
    """
    Utility class for deleting files based on specific criteria.

    Parameters:
        folder_path (str): The folder path where the deletion takes place.

    Attributes:
        deleted_files (list[str]): A list of all files that where deleted in the process.
        deleted_files_by_extension (dict[str, list[str]]): A dictionary containing the files (value)
            associated which each extension (key) that where deleted in the process.
    """
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.deleted_files = []
        self.deleted_files_by_extension = {}

    def delete_by_single_extension(self, file_extension: str) -> None:
        """
        Delete files with a specific extension.

        Parameters:
            file_extension (str): The file extension used for filtering and deletion.

        Returns:
            None
        """
        files = os.listdir(self.folder_path)
        for file in files:
            if file.endswith(file_extension):
                os.remove(os.path.join(self.folder_path, file))
                self.deleted_files_by_extension[file_extension] = file

    def delete_by_multiple_extensions(self, list_of_file_extensions: str) -> None:
        """
        Delete files with multiple specified extensions.

        Parameters:
            list_of_file_extensions (str): A comma-separated string of file extensions for
                filtering and deletion.

        Returns:
            None
        """
        cleaned_list_of_file_extensions = reusable_functions.split_extensions(list_of_file_extensions)
        for clean_extension in cleaned_list_of_file_extensions:
            self.delete_by_single_extension(clean_extension)

    def delete_by_keyword(self, name_keyword: str, list_of_file_extensions: str = ''):
        """
        Deleting a set of files using a specific extension provided by the user.

        Parameters:
            name_keyword (str): The keyword substring that will be matched in the targeted file/files.
            list_of_file_extensions (str, optional): A string of file extensions separated by commas.

        Returns:
            None
        """
        cleaned_list_of_file_extensions = reusable_functions.split_extensions(list_of_file_extensions)
        files = os.listdir(self.folder_path)
        for index, file in enumerate(files, start=1):
            if cleaned_list_of_file_extensions:
                if name_keyword in os.path.splitext(file)[0] and os.path.splitext(file)[1][1:] in cleaned_list_of_file_extensions:
                    os.remove(os.path.join(self.folder_path, os.path.splitext(file)[0] + os.path.splitext(file)[1]))
                    self.deleted_files_by_extension[os.path.splitext(file)[1][1:]] = file
            else:
                if name_keyword in os.path.splitext(file)[0]:
                    os.remove(os.path.join(self.folder_path, file))
                    self.deleted_files.append(file)
