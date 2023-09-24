import os


class Search:
    """
    Utility class for searching within a specific file path while offering different types of search
    criteria tailored to the user's needs.

    Parameters:
        folder_path (str): The folder path where the search takes place.

    Attributes:
        file_list_by_name (list[str]): A list of files found when searching by name or by both
            name and extension. This list contains the filenames that match the search criteria.
        file_list_by_ext (list[str]): A list of files found when searching by extension.
            This list contains filenames that have the specified extension.
    """
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.file_list_by_name = []
        self.file_list_by_ext = []

    def search_by_name(self, file_name: str, file_extension: str) -> bool:
        """
        Finds a file or a series of files based on the information provided by the user
        in the search functionality additional window.

        Parameters:
            file_name (str): The name of the file.
            file_extension (str): The extension of the file.

        Returns:
            bool: True if the list is not empty, False otherwise.

        Notes:
            The function can receive an extension which has a different role in comparison with
            the 'search_by_extension' function.
            A. Searching only by name will include the files with the same name but different
            extensions (if applicable), so the function can find one or more results.
            B. Searching by both name and extension will ensure a single finding since both the
            name and the extension are ensuring the uniqueness of the file.
        """
        files = os.listdir(self.folder_path)
        for file in files:
            if ((os.path.splitext(file)[0] == file_name or file_name in os.path.splitext(file)[0])
                    and (not file_extension or file.endswith('.' + file_extension))):
                self.file_list_by_name.append(file)

        return bool(self.file_list_by_name)

    def search_by_extension(self, file_extension: str) -> bool:
        """
        Finds all the files with the specified extension, regardless of their names.

        Parameters:
            file_extension (str): The extension of the file/files.

        Returns:
            bool: True if the list is not empty, False otherwise.
        """
        files = os.listdir(self.folder_path)
        for file in files:
            if file.endswith('.' + file_extension):
                self.file_list_by_ext.append(file)

        return bool(self.file_list_by_name)
