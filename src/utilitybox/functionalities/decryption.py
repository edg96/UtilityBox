import os

from cryptography.fernet import Fernet

from src.utilitybox.auxiliar import reusable_functions


class Decryption:
    """
    Utility class for decrypting a file using a specific key.

    Parameters:
        file_path (str): The folder path where the file is located.

    Attributes:
        file_key_pair (dict[str, str]): The pair that contains file name and it's associated key.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_key_pair = {}

    def load_key(self) -> bytes:
        """
        Load the encryption key associated with the file.

        Returns:
            bytes: The encryption key as bytes.
        """
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        default_key_path = reusable_functions.get_project_keys_path()
        key_location = os.path.join(default_key_path, file_name + '.key')
        self.file_key_pair[file_name] = key_location
        return open(key_location, 'rb').read()

    def remove_key(self) -> None:
        """
        Remove the encryption key file associated with the decrypted file.

        Returns:
            None
        """
        default_key_path = reusable_functions.get_project_keys_path()
        key_path = os.path.join(default_key_path, os.path.splitext(os.path.basename(self.file_path))[0] + '.key')
        os.remove(key_path)

    def decrypt_file(self, key: bytes) -> None:
        """
        Decrypt the file using the provided encryption key.

        Parameters:
            key (bytes): The encryption key as bytes.

        Returns:
            None
        """
        fernet = Fernet(key)

        message = reusable_functions.read_from_file_by_line(self.file_path, 'rb')
        decrypted_message = fernet.decrypt(message)
        reusable_functions.write_to_file(self.file_path, decrypted_message, 'wb')

        self.remove_key()
