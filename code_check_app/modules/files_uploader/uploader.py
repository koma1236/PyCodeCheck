"""
Module: uploader.py

This module contains the Uploader class which is responsible for handling file uploads by users.

Classes:
- Uploader: Class to handle file uploads by users.

Methods:
- init(request: WSGIRequest): Initializes the Uploader object with the given request.
- check_paths(): Checks if the upload and user paths exist, and creates them if not.
- upload_user_files(): Uploads the user files to the server and updates the file data
"""

import os
from typing import List
from django.core.handlers.wsgi import WSGIRequest
from django.core.files.uploadedfile import InMemoryUploadedFile
from code_check_app.modules.base import base_exec


class Uploader:
    """
    Class to handle file uploads by users.
    """

    def __init__(self, request: WSGIRequest):
        """
        Initializes the Uploader object with the given request.

        Args:
        - request: WSGIRequest object representing the HTTP request.
        """
        self.request: WSGIRequest = request
        self.upload_path = os.path.abspath('./uploads')
        self.user_path = os.path.join(self.upload_path, f'{request.user.id}')
        self.files: List[InMemoryUploadedFile] = self.request.FILES.getlist('files')

    def check_paths(self):
        """
        Checks if the upload and user paths exist, and creates them if not.
        """
        if not os.path.isdir(self.upload_path):
            os.mkdir(self.upload_path)
        if not os.path.isdir(self.user_path):
            os.mkdir(self.user_path)

    def upload_user_files(self):
        """
        Uploads the user files to the server and updates the file data in the database.
        """
        self.check_paths()
        for file in self.files:
            file_path = os.path.join(self.user_path, file.name)
            if os.path.isfile(file_path):
                # File already exists, update metadata in the database
                base_exec.update_file(file.name, self.request.user.id)
                os.remove(file_path)
            else:
                # File does not exist, create new file metadata in the database
                base_exec.write_new_file_params(self.request.user.id, file_path, file.name)
            with open(file_path, 'wb+') as file_write:
                for chunk in file.chunks():
                    file_write.write(chunk)
