import os
import calendar
from datetime import date

from auxiliar import reusable_functions


class LogConfigurer:
    """
    Utility class for configuring and managing log files and directories.
    This class provides methods for creating and organizing log directories based on the
    current year, month and the functionalities that are available through the application.

    Attributes:
        logging_default_path (str): The default path where log directories are created.
        year_folder_path (str): The path of the current year's log directory.
        month_folder_path (str): The path of the current month's log directory.
        year_folder_created (bool): Flag indicating whether the year folder has been created.
        month_folder_created (bool): Flag indicating whether the month folder has been created.
        datetimeday (int): The current day of the month.
        datetimemonth (int): The current month.
        datetimeyear (int): The current year.
    """
    def __init__(self):
        self.logging_default_path = reusable_functions.get_project_logs_path()
        self.year_folder_path = 'Not created'
        self.month_folder_path = 'Not created'
        self.year_folder_created = False
        self.month_folder_created = False
        self.datetimeday = date.today().day
        self.datetimemonth = date.today().month
        self.datetimeyear = date.today().year

    def get_year_folder_path(self) -> str:
        """
        Get the path of the current year's log directory.

        Returns:
            str: The path of the year's log directory.
        """
        self.check_and_create_year_folder()

        return self.year_folder_path

    def get_month_folder_path(self) -> str:
        """
        Get the path of the current month's log directory.

        Returns:
            str: The path of the month's log directory.
        """
        self.check_and_create_month_folder()

        return self.month_folder_path

    def give_log_name(self) -> str:
        """
        Generate a log file name based on the current date.

        Returns:
            str: The generated log file name.
        """
        log_name = str(self.datetimeday) + '_ublog'
        return log_name

    def check_and_create_year_folder(self) -> None:
        """
        Create the current year's log directory if it doesn't exist.

        Returns:
            None
        """
        year_folder_path = os.path.join(self.logging_default_path, str(self.datetimeyear))
        if not os.path.exists(year_folder_path):
            os.mkdir(year_folder_path)
        self.year_folder_created = True
        self.year_folder_path = year_folder_path

    def check_and_create_month_folder(self) -> None:
        """
        Create the current month's log directory if it doesn't exist.

        Returns:
            None
        """
        month_name = calendar.month_name[self.datetimemonth]
        month_folder_path = os.path.join(self.logging_default_path, str(self.datetimeyear), month_name)
        if not os.path.exists(month_folder_path):
            os.mkdir(month_folder_path)
        self.month_folder_created = True
        self.month_folder_path = month_folder_path

    def create_category(self) -> None:
        """
        Create subfolders for different categories (based on the functionalities that are
        available through the application) within the month directory.

        Returns:
            None
        """
        functionalities = ['Search', 'Sort', 'Delete', 'Encryption', 'Decryption', 'Compress', 'Decompress']
        if self.month_folder_created and self.year_folder_created:
            for functionality in functionalities:
                category_path = os.path.join(self.month_folder_path, functionality)
                if not os.path.exists(category_path):
                    os.mkdir(category_path)
