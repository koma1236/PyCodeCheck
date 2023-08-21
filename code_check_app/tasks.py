"""
Module: Tasks

This module contains tasks for performing code checks on uploaded files and
 sending email notifications to users.

Functions:
- pylint_check: Task to perform pylint check on uploaded files.
- send_email: Task to send email containing the check results to the user.
"""
from io import StringIO
from celery import shared_task
from pylint.lint import Run
from pylint.reporters.text import TextReporter
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from code_check_app.modules.base import base_exec


@shared_task
def pylint_check():
    """
    Task to perform pylint check on uploaded files.
    Retrieves files for check using base_exec.get_files_for_check().
    Runs pylint on each file and saves the check result using base_exec.set_check_result().
    Sends email with the check results to the user using send_email() task.
    """
    files = base_exec.get_files_for_check()
    for file in files:
        stdout = StringIO()
        reporter = TextReporter(stdout)
        Run(['--disable=F0401', file.upload_path], reporter=reporter, exit=False)
        check_log = reporter.out.getvalue()
        base_exec.set_check_result(file.file_name, check_log, file.uploaded_by_user_id)

        user_email = file.user.email
        mail_theme = f'Результат проверки "{file.file_name}"'
        mail_message = check_log
        user_id = file.user.id
        send_email.delay(user_email, mail_theme, mail_message, user_id)


@shared_task()
def send_email(user_email: str, mail_theme: str, mail_message: str, user_id: int):
    """
    Task to send email containing the check results to the user.

    Args:
        user_email (str): Email address of the user.
        mail_theme (str): Subject of the email.
        mail_message (str): Body of the email.
        user_id (int): ID of the user.

    Uses Django's EmailMessage to create and send the email.
    """
    with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = mail_theme
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_email, ]
        message = mail_message
        EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()

    base_exec.create_message(user_id, mail_theme, mail_message)
