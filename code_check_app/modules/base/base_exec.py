from typing import List
import os
from django.utils import timezone
from code_check_app.models import UserFiles, UsersMail


def write_new_file_params(user_id: int, upload_path: str, file_name: str):
    """
    Saves the parameters of a new file uploaded by a user.

    Args:
    - user_id (int): The ID of the user who uploaded the file.
    - upload_path (str): The path where the file is stored.
    - file_name (str): The name of the file.

    Returns:
    - None
    """

    UserFiles(
        file_name=file_name,
        uploaded_by_user_id=user_id,
        upload_path=upload_path,
    ).save()


def update_file(file_name: str, user_id: int):
    """
    Updates the information of a file including the change date and check result.

    Args:
    - file_name (str): The name of the file.
    - user_id (int): The ID of the user who uploaded the file.

    Returns:
    - None
    """

    file_model: UserFiles = UserFiles.objects.get(file_name=file_name, uploaded_by_user_id=user_id)
    file_model.change_date = timezone.now()
    file_model.check_result = 'Ожидает проверки'
    file_model.new_file = True
    file_model.save()


def set_check_result(file_name: str, check_log: str, user_id: int):
    """
    Sets the check result and check log for a file.

    Args:
    - file_name (str): The name of the file.
    - check_log (str): The result of the file check.
    - user_id (int): The ID of the user who uploaded the file.

    Returns:
    - None
    """

    file_model: UserFiles = UserFiles.objects.get(file_name=file_name, uploaded_by_user_id=user_id)
    file_model.check_result = 'Проверен'
    file_model.new_file = False
    file_model.check_log = check_log
    file_model.save()


def delete_file(file_id: int):
    """
    Deletes a file and its corresponding record from the database.

    Args:
    - file_id (int): The ID of the file in the database.

    Returns:
    - None
    """

    file_model: UserFiles = UserFiles.objects.get(id=int(file_id))
    os.remove(file_model.upload_path)
    file_model.delete()


def get_files_for_check() -> List[UserFiles]:
    """
    Retrieves all the files that are waiting for checking.

    Returns:
    - List[UserFiles]: A list of UserFiles objects.
    """

    files = UserFiles.objects.filter(new_file=True)
    return files


def create_message(user_id: int, mail_theme: str, mail_message: str):
    """
    Creates a new email message to be sent to a user.

    Args:
    - user_id (int): The ID of the user who will receive the email.
    - mail_theme (str): The subject of the email.
    - mail_message (str): The content of the email.

    Returns:
    - None
    """

    UsersMail(
        user_id=user_id,
        mail_send_date=timezone.now(),
        mail_theme=mail_theme,
        mail_message=mail_message,
    ).save()
