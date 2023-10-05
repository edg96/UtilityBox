import os

from cryptography.fernet import Fernet

from src.utilitybox.auxiliar import reusable_functions


class Encryption:
    """
    Utility class for encrypting a file text and allocating it a specific key that can decrypt it.

    Parameters:
        file_path (str): The folder path where the file is located.

    Attributes:
        file_key_pair (dict[str, str]): A dictionary containing the file name of the encrypted text file
            and the full path associated with the key that was generated in the process.
    """
    # The default path where the keys are stored
    # Keys names are a one to one match with the name of the text file for easy association
    default_key_folder = reusable_functions.get_project_keys_path()

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_key_pair = {}

    def generate_key(self, key_path: str = default_key_folder) -> None:
        """
        Generate a new encryption key and save it to a key type file.

        Parameters:
            key_path (str, optional): The path where the encryption key file will be saved.
                Defaults to the class's default_key_path.
        """
        os.chdir(key_path)
        key = Fernet.generate_key()
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        with open(file_name + '.key', 'wb') as key_file:
            key_file.write(key)
        self.file_key_pair[file_name] = os.path.join(self.default_key_folder, file_name + '.key')

    def load_key(self) -> bytes:
        """
        Load the encryption key from a file.

        Returns:
            bytes: The encryption key loaded from the key file.
        """
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        return open(file_name + '.key', 'rb').read()

    def encrypt_file(self, key: bytes) -> None:
        """
        Encrypt the contents of the file using the provided encryption key.

        Parameters:
            key (bytes): The encryption key associated with a specific file.
        """
        fernet = Fernet(key)

        data_from_file = reusable_functions.read_from_file_by_line(self.file_path, 'rb')
        encrypted_data = fernet.encrypt(bytes(data_from_file))
        reusable_functions.write_to_file(self.file_path, encrypted_data, 'wb')
