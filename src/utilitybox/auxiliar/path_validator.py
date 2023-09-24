import os


def check_path_existence(folder_path: str) -> bool:
    """
    Check if a folder or file path exists.

    Parameters:
        folder_path (str): The path of the folder or file to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    return os.path.exists(folder_path)


class PathValidator:
    """
    Utility class that is instantiated with a folder or file path that can be changed as needed.

    Parameters:
        folder_path (str): The path to the folder or file.
    """
    def __init__(self, folder_path):
        self.folder_path = folder_path
