import os
import shutil
import zipfile

import patoolib

from auxiliar import reusable_functions


class Archive:
    """
    Utility class for compressing or decompressing files.

    Attributes:
        default_path (str): The default folder path where the archives will be
            compressed or decompressed if no specific destination is provided (default path: Desktop).
    """
    def __init__(self):
        self.default_path = reusable_functions.get_system_path()

    def compress_zip_files(self, archive_name: str, files_list: list[str], destination_path: str = '') -> None:
        """
        Compress a list of files into a ZIP archive.

        Parameters:
            archive_name (str): The name of the ZIP archive.
            files_list (list[str]): The list of files to be compressed (full path files).
            destination_path (str, optional): The destination folder for the archive.
                Defaults to the default path if not specified.

        Returns:
            None
        """
        if not destination_path:
            destination_path = self.default_path
        os.chdir(os.path.join(destination_path, 'archives'))
        with zipfile.ZipFile(archive_name + '.zip', 'w') as zipf:
            for file in files_list:
                zipf.write(file, arcname=os.path.basename(file))
        os.chdir(self.default_path)

    def decompress_zip_files(self, archive_file_path: str, destination_path: str = '') -> None:
        """
        Decompress a ZIP archive.

        Parameters:
            archive_file_path (str): The path of the ZIP archive.
            destination_path (str, optional): The destination folder for the content of the archive.
                Defaults to the default path if none is specified.

        Returns:
            None
        """
        if not destination_path:
            destination_path = self.default_path
        os.chdir(destination_path)
        with zipfile.ZipFile(archive_file_path, 'r') as zipf:
            zipf.extractall()
        os.chdir(self.default_path)

    def compress_rar_files(self, archive_name: str, files_list: list[str], destination_path: str = '') -> None:
        """
        Compress a list of files into a RAR archive.

        Parameters:
            archive_name (str): The name of the RAR archive.
            files_list (list[str]): The list of files to be compressed (full path files).
            destination_path (str, optional): The destination folder for the archive.
                Defaults to the default path if not specified.

        Returns:
            None
        """
        if not destination_path:
            destination_path = self.default_path
        os.chdir(os.path.join(destination_path, 'archives'))
        patoolib.create_archive(archive_name + '.rar', files_list)
        os.chdir(self.default_path)

    def decompress_rar_files(self, archive_file_path: str, destination_path: str = '') -> None:
        """
        Decompress a RAR archive.

        Parameters:
            archive_file_path (str): The path of the RAR archive.
            destination_path (str, optional): The destination folder for the content of the archive.
                Defaults to the default path if none is specified.

        Returns:
            None
        """
        if not destination_path:
            destination_path = self.default_path
        patoolib.extract_archive(archive_file_path, outdir=destination_path, interactive=False)
        os.chdir(self.default_path)

    def transfer_to_temporary_folder(self, files_list: list[str], destination_path: str = '') -> None:
        """
        Creates copies of files in a temporary folder to avoid the creation of a subtree style
        structure containing all the subfolders leading to a file.

        Parameters:
            files_list (list[str]): The list of files to be moved.
            destination_path (str, optional): The destination folder for the files.
                Defaults to the default path if none is specified.

        Returns:
            None
        """
        if not destination_path:
            destination_path = self.default_path
        temp_dir = os.path.join(destination_path, 'archives')
        os.makedirs(temp_dir, exist_ok=True)
        os.chdir(destination_path)
        for file in files_list:
            shutil.copy(file, temp_dir)
        os.chdir(self.default_path)

    def clean_files(self, file_list: list[str], targeted_path: str = '') -> None:
        """
        Clean the files that are present in a folder based on a specified list of files.

        Parameters:
            files_list (list[str]): The list of files to be cleaned.
            targeted_path (str, optional): The folder path where the files are located.
                Defaults to the default path if none is specified.

        Notes:
            Recommended to be used in conjunction with the 'transfer_to_temporary_folder' function.
            Should be used together in the following order:
                A: temporary transfer the files
                B: start compressing
                C: clean the folder of the copies

        Returns:
            None
        """
        if not targeted_path:
            targeted_path = self.default_path
        targeted_path = os.path.join(targeted_path, 'archives')

        try:
            os.chdir(targeted_path)
        except FileNotFoundError as fnfe:
            print('Changing directory Error: \n\t' + str(fnfe))

        for file in file_list:
            print(file)
            try:
                os.remove(file)
            except FileNotFoundError as fnfe:
                print('Removing file Error: \n\t' + str(fnfe))

        os.chdir(self.default_path)

        try:
            files = os.listdir(targeted_path)
            if len(files) == 0:
                os.rmdir(targeted_path)
        except FileNotFoundError as fnfe:
            print('Changing directory Error: \n\t' + str(fnfe))
