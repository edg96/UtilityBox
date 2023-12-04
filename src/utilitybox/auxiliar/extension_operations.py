import os


def split_extensions(list_of_file_extensions: str) -> list[str]:
    """
    Split a string of file extensions separated by commas into a list of extensions.

    Params:
        list_of_file_extensions (str): A string of file extensions separated by commas.
    """
    cleaned_list_of_file_extensions = []
    new_found_extension = ''
    for letter in list_of_file_extensions:
        if letter != ',':
            new_found_extension += letter
        else:
            cleaned_list_of_file_extensions.append(new_found_extension.replace(' ', ''))
            new_found_extension = ''
    cleaned_list_of_file_extensions.append(new_found_extension.replace(' ', ''))

    return cleaned_list_of_file_extensions


def group_files_by_extensions(list_of_files) -> dict[str, list[str]]:
    """
    Group a list of file paths based on their extensions into a dictionary.

    Params:
        list_of_files (list[str]): A list of file paths.
    """
    grouped_list = {}
    for file in list_of_files:
        file_name, file_extension = os.path.splitext(file)
        file_extension = file_extension[1:]
        if file_extension not in grouped_list.keys():
            grouped_list[file_extension] = []
        grouped_list[file_extension].append(file_name)

    return grouped_list
