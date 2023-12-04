import os
from pathlib import Path


def get_system_path() -> str:
    """
    Get the system's default path for file operations (usually the desktop).
    """
    return os.path.join(os.path.expanduser('~'), 'Desktop')


def get_project_folder() -> Path:
    """
    Get the project's root.
    """
    return Path(__file__).resolve().parent.parent.parent.parent


def get_project_keys_path() -> str:
    """
    Get the root path of the project where this script is located for key files.
    """
    return os.path.join(get_project_folder(), 'resources', 'results', 'keys')


def get_project_icons_path() -> str:
    """
    Get the root path of the project where this script is located for icon files.
    """
    return os.path.join(get_project_folder(), 'resources', 'icons')
