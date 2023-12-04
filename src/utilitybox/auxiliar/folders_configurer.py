import os
import calendar
from datetime import date

from src.utilitybox.auxiliar.project_paths import get_project_folder


class FoldersConfigure:
    """
    Utility class for configuring and managing the application directories.

    This class is responsible for checking the existence of the application's necessary directories,
    recreating the missing ones, and ensuring the integrity of the application directory hierarchy.

    Attributes:
        self.datetimeday (int): The current day of the month.
        self.datetimemonth (int): The current month.
        self.datetimeyear (int): The current year.
        self.results_folder_exists (bool): Flag indicating whether the results folder has been created.
        self.logs_folder_exists (bool): Flag indicating whether the logs folder has been created.
        self.year_folder_exists (bool): Flag indicating whether the year folder has been created.
        self.month_folder_exists (bool): Flag indicating whether the month folder has been created.
        self.keys_folder_exists (bool): Flag indicating whether the keys folder has been created.
        self.updated_year_folder_path (str): The path of the current year's log directory.
        self.updated_month_folder_path (str): The path of the current month's log directory.
    """

    def __init__(self):
        """
        Initialize the FoldersConfigure object.
        """
        self.datetimeday = date.today().day
        self.datetimemonth = date.today().month
        self.datetimeyear = date.today().year
        self.results_folder_exists = False
        self.logs_folder_exists = False
        self.year_folder_exists = False
        self.month_folder_exists = False
        self.keys_folder_exists = False
        self.updated_year_folder_path = None
        self.updated_month_folder_path = None

    @staticmethod
    def generate_default_results_folder_path() -> str:
        """
        Provides the default path of the 'results' folder.
        """
        project_root = get_project_folder()
        results_folder_path = os.path.join(project_root, 'resources', 'results')

        return results_folder_path

    @staticmethod
    def generate_default_logs_folder_path() -> str:
        """
        Provides the default path of the 'logs' folder.
        """
        project_root = get_project_folder()
        logs_folder_path = os.path.join(project_root, 'resources', 'results', 'logs')

        return logs_folder_path

    @staticmethod
    def generate_default_keys_folder_path() -> str:
        """
        Provides the default path of the 'keys' folder.
        """
        project_root = get_project_folder()
        keys_folder_path = os.path.join(project_root, 'resources', 'results', 'keys')

        return keys_folder_path

    def generate_default_year_folder_path(self) -> str:
        """
        Provides the default path of the year folder.
        """
        year_folder_path = os.path.join(self.generate_default_logs_folder_path(), str(self.datetimeyear))

        return year_folder_path

    def generate_default_month_folder_path(self) -> str:
        """
        Provides the default path of the month folder.
        """
        month_name = calendar.month_name[self.datetimemonth]
        month_folder_path = os.path.join(self.generate_default_logs_folder_path(), str(self.datetimeyear), month_name)

        return month_folder_path

    def _check_if_results_folder_exists(self) -> None:
        """
        Checks if the results folder exists and updates the associated variable of existence.
        """
        results_folder_path = self.generate_default_results_folder_path()
        if os.path.exists(results_folder_path):
            self.results_folder_exists = True
        else:
            self.results_folder_exists = False

    def _check_if_logs_folder_exists(self) -> None:
        """
        Checks if the logs folder exists and updates the associated variable of existence.
        """
        logs_folder_path = self.generate_default_logs_folder_path()
        if os.path.exists(logs_folder_path):
            self.logs_folder_exists = True
        else:
            self.logs_folder_exists = False

    def _check_if_year_folder_exists(self) -> None:
        """
        Checks if the year folder exists and updates the associated variable of existence.
        """
        year_folder_path = self.generate_default_year_folder_path()
        if os.path.exists(year_folder_path):
            self.year_folder_exists = True
        else:
            self.year_folder_exists = False

    def _check_if_month_folder_exists(self) -> None:
        """
        Checks if the month folder exists and updates the associated variable of existence.
        """
        month_folder_path = self.generate_default_month_folder_path()
        if os.path.exists(month_folder_path):
            self.month_folder_exists = True
        else:
            self.month_folder_exists = False

    def _check_if_keys_folder_exists(self) -> None:
        """
        Checks if the keys folder exists and updates the associated variable of existence.
        """
        keys_folder_path = self.generate_default_keys_folder_path()
        if os.path.exists(keys_folder_path):
            self.keys_folder_exists = True
        else:
            self.keys_folder_exists = False

    def _create_results_folder(self) -> None:
        """
        Creates the results folder if it doesn't exist.
        """
        results_folder_path = self.generate_default_results_folder_path()
        os.mkdir(results_folder_path)

    def _create_logs_folder(self) -> None:
        """
        Creates the logs folder if it doesn't exist.
        """
        logs_folder_path = self.generate_default_logs_folder_path()
        os.mkdir(logs_folder_path)

    def _create_year_folder(self) -> None:
        """
        Creates the year folder if it doesn't exist.
        """
        year_folder_path = self.generate_default_year_folder_path()
        os.mkdir(year_folder_path)

    def _create_month_folder(self) -> None:
        """
        Creates the month folder if it doesn't exist.
        """
        month_folder_path = self.generate_default_month_folder_path()
        os.mkdir(month_folder_path)

    def _create_keys_folder(self) -> None:
        """
        Creates the keys folder if it doesn't exist.
        """
        keys_folder_path = self.generate_default_keys_folder_path()
        os.mkdir(keys_folder_path)

    def _create_category(self) -> None:
        """
        Creates folders for different categories (based on the functionalities that are
        available through the application) within the month directory.
        """
        functionalities = ['Search', 'Sort', 'Delete', 'Encryption', 'Decryption', 'Compress', 'Decompress']
        month_folder_path = self.generate_default_month_folder_path()
        if self.results_folder_exists and self.logs_folder_exists:
            if self.year_folder_exists and self.month_folder_exists:
                for functionality in functionalities:
                    category_path = os.path.join(month_folder_path, functionality)
                    if not os.path.exists(category_path):
                        os.mkdir(category_path)

    def check_folders_setup(self) -> None:
        """
        Checks for missing folders in the setup and creates the missing ones.
        """
        self._check_if_results_folder_exists()
        if not self.results_folder_exists:
            self._create_results_folder()

        self._check_if_logs_folder_exists()
        if not self.logs_folder_exists:
            self._create_logs_folder()

        self._check_if_year_folder_exists()
        if not self.year_folder_exists:
            self._create_year_folder()

        self._check_if_month_folder_exists()
        if not self.month_folder_exists:
            self._create_month_folder()

        self._check_if_keys_folder_exists()
        if not self.keys_folder_exists:
            self._create_keys_folder()

        self._create_category()

    def give_log_name(self) -> str:
        """
        Generate a log file name based on the current date.

        Returns:
            str: The generated log file name.
        """
        log_name = str(self.datetimeday) + '_ublog.txt'
        return log_name

    def get_year_folder_path(self) -> str:
        """
        Get the path of the current year's log directory.

        Returns:
            str: The path of the year's log directory.
        """
        return self.updated_year_folder_path

    def get_updated_month_folder_path(self) -> str:
        """
        Get the path of the current month's log directory.

        Returns:
            str: The path of the month's log directory.
        """
        return self.updated_month_folder_path
