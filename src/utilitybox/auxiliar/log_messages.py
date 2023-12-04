def convert_slashes(path) -> str:
    """
    Convert forward slashes to backslashes in a given path.

    Params:
        path (str): The input path.
    """
    return path.replace('/', '\\')


def success_message(operation_unique_identifier: str, operation_id: int) -> str:
    """
    Generates a success message and returns it as a string.

    Params:
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): A HTTP code indicating the state of the result of the operation.
    """
    if operation_id == 200:
        return (f'[{operation_unique_identifier.upper()} {operation_id}]:'
                f'\nSuccess: changes performed.')
    elif operation_id == 204:
        return (f'[{operation_unique_identifier.upper()} {operation_id}]:'
                f'\nSuccess: no changes performed.')


def path_invalid_message(operation_unique_identifier: str, operation_id: int, location_path: str = '') -> str:
    """
    Construct a detailed result message to be logged, indicating an invalid path.

    Params:
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): A HTTP code indicating the state of the result of the operation.
        location_path (str): The path of a file or folder where the operation takes place.
    """
    location_path_formatted = convert_slashes(location_path)
    if not location_path_formatted:
        return (f'[{operation_unique_identifier.upper()}: {operation_id}]:'
                f'\n\tInvalid path:'
                f'\n\t\tEmpty path')
    else:
        return (f'[{operation_unique_identifier.upper()}: {operation_id}]:'
                f'\n\tInvalid path:'
                f'\n\t\t{location_path_formatted}')


def simple_success_message(operation_unique_identifier: str, operation_id: int) -> str:
    """
    Generates a simplified success message and returns it as a string.

    Params:
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): A HTTP code indicating the state of the result of the operation.
    """
    if operation_id == 200:
        return f'[{operation_unique_identifier.upper()} {operation_id}]: Success: changes performed'
    elif operation_id == 204:
        return f'[{operation_unique_identifier.upper()} {operation_id}]: Success: no changes performed'


def simple_path_invalid_message(operation_unique_identifier: str, operation_id: int) -> str:
    """
    Construct a simplified result message to be logged, indicating an invalid path.

    Params:
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): A HTTP code indicating the state of the result of the operation.
    """
    return f'[{operation_unique_identifier.upper()}: {operation_id}]: Failure: Invalid path'


def update_display_log(mainbox, operation_unique_identifier: str, operation_id: int) -> None:
    """
    Construct a message based on an operation id (HTTP codes association) and pass it to the MainBox
    widget to be displayed to the user.

    Params:
        mainbox (MainBox): An instance of the MainBox class (parent).
        operation_unique_identifier (str): The operation identifier that specifies the type of operation.
        operation_id (int): A HTTP code indicating the state of the result of the operation.
    """
    log_frame_message, operation_status_color = '', ''

    if operation_id == 200:
        operation_status_color = '#009137'
        log_frame_message = simple_success_message(operation_unique_identifier, operation_id)
    elif operation_id == 204:
        operation_status_color = '#006571'
        log_frame_message = simple_success_message(operation_unique_identifier, operation_id)
    elif operation_id == 404:
        operation_status_color = '#912800'
        log_frame_message = simple_path_invalid_message(operation_unique_identifier, operation_id)

    mainbox.update_log(True, log_frame_message, operation_status_color)
