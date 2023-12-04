import os.path

from src.utilitybox.auxiliar.extension_operations import split_extensions


class Delete:
    """
    Utility class for deleting files based on specific criteria.

    Attributes:
        self.folder_path (str): The folder path where the deletion takes place.
        self.files_deleted (list[str]): A list of all files that were deleted in the process.
    """

    def __init__(self, folder_path: str):
        """
        Initialize the Delete object.

        Params:
            folder_path (str): The folder path where the deletion takes place.
        """
        self.folder_path = folder_path
        self.files_deleted = []

    def delete_by_single_extension(self, file_extension: str) -> None:
        """
        Delete files with a specific extension.

        Params:
            file_extension (str): The file extension used for filtering and deletion.
        """
        files = os.listdir(self.folder_path)
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(self.folder_path, file)
                os.remove(file_path)
                self.files_deleted.append(file_path)

    def delete_by_multiple_extensions(self, list_of_file_extensions: str) -> None:
        """
        Delete files with multiple specified extensions.

        Params:
            list_of_file_extensions (str): A comma-separated string of file extensions for
                filtering and deletion.
        """
        cleaned_list_of_file_extensions = split_extensions(list_of_file_extensions)
        for clean_extension in cleaned_list_of_file_extensions:
            self.delete_by_single_extension(clean_extension)

    def delete_by_keyword(self, name_keyword: str, list_of_file_extensions: str = '') -> None:
        """
        Deleting a set of files using a specific extension provided by the user.

        Params:
            name_keyword (str): The keyword substring that will be matched in the targeted file/files.
            list_of_file_extensions (str, optional): A string of file extensions separated by commas.
        """
        cleaned_list_of_file_extensions = split_extensions(list_of_file_extensions)
        files = os.listdir(self.folder_path)
        for file in files:
            current_file_name, current_file_extension = os.path.splitext(file)
            if cleaned_list_of_file_extensions:
                if name_keyword in current_file_name and current_file_extension[1:] in cleaned_list_of_file_extensions:
                    file_path = os.path.join(self.folder_path, file)
                    os.remove(file_path)
                    self.files_deleted.append(file_path)
            else:
                if name_keyword in current_file_name:
                    file_path = os.path.join(self.folder_path, file)
                    os.remove(file_path)
                    self.files_deleted.append(file_path)
