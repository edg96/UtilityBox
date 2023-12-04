import os

from cryptography.fernet import Fernet

from src.utilitybox.auxiliar.project_paths import get_project_keys_path


class Decryption:
    """
    Utility class for decrypting a file using a specific key.

    Attributes:
        self.file_path (str): The file path of the encrypted file.
        self.file_key_pair (dict[str, str]): A dictionary containing the file name and its associated key file path.
    """

    def __init__(self, file_path: str):
        """
        Initialize the Decryption object.

        Params:
            file_path (str): The file path of the encrypted file.
        """
        self.file_path = file_path
        self.file_key_pair = {}

    def load_key(self) -> bytes:
        """
        Load the encryption key associated with the file.
        """
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        default_key_path = get_project_keys_path()
        key_location = os.path.join(default_key_path, file_name + '.key')
        self.file_key_pair[file_name] = key_location
        return open(key_location, 'rb').read()

    def remove_key(self) -> None:
        """
        Remove the encryption key file associated with the decrypted file.
        """
        default_key_path = get_project_keys_path()
        key_path = os.path.join(default_key_path, os.path.splitext(os.path.basename(self.file_path))[0] + '.key')
        os.remove(key_path)

    def decrypt_file(self, key: bytes) -> None:
        """
        Decrypt the file using the provided encryption key.

        Params:
            key (bytes): The encryption key as bytes.
        """
        fernet = Fernet(key)

        with open(self.file_path, 'rb') as file:
            encrypted_message = file.read()

        decrypted_message = fernet.decrypt(encrypted_message)

        with open(self.file_path, 'wb') as file:
            file.write(decrypted_message)

        self.remove_key()
