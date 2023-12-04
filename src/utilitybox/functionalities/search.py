import os


class Search:
    """
    Utility class for searching within a specific file path while offering different types of search
    criteria tailored to the user's needs.

    Attributes:
        self.files_found (list[str]): A list of files found when searching by name or by both
            name and extension.
    """

    def __init__(self, folder_path: str):
        """
        Initialize the Search object.

        Params:
            folder_path (str): The folder path where the search takes place.
        """
        self.folder_path = folder_path
        self.files_found = []

    def search_by_name(self, file_name: str, file_extension: str) -> None:
        """
        Finds a file or a series of files based on the information provided by the user
        in the search functionality additional window.

        Params:
            file_name (str): The name of the file.
            file_extension (str): The extension of the file.

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
                self.files_found.append(file)

    def search_by_extension(self, file_extension: str) -> None:
        """
        Finds all the files with the specified extension, regardless of their names.

        Params:
            file_extension (str): The extension of the file/files.

        Returns:
            bool: True if the list is not empty, False otherwise.
        """
        files = os.listdir(self.folder_path)
        for file in files:
            if file.endswith('.' + file_extension):
                self.files_found.append(file)
