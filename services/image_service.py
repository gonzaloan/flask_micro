
"""
Class to abstract the service layer of the application to keep controller layer simplified.
"""
from flask import make_response
from exceptions.exceptions import InvalidUsage, InternalErrorUsage
from utils.constants import INVALID_FILE_RESPONSE, ERROR_RESPONSE, GENERATED_FILE_RESPONSE, MAC_AUTO_GENERATED_FILES, \
    ERROR_ZIP_FILE_RESPONSE
from utils.utils import MicroUtils
import os
import zipfile
import shutil


class ImagesService:

    @classmethod
    def attach_image(cls, file, app):
        app.logger.debug(f'Processing inside Images Service file: {file.filename}')
        if file.filename == '' or not MicroUtils.allowed_file(file.filename):
            app.logger.error('Error while attach_picture request. The file is not valid')
            raise InvalidUsage(INVALID_FILE_RESPONSE, status_code=400)

        # If this is a zip file
        if MicroUtils.is_zip_file(file.filename):
            return make_response(cls.get_upload_zip_file_response(app, file), 201)

        new_file_path = cls.save_image_and_get_link(app, file)
        response = GENERATED_FILE_RESPONSE
        response['path'] = new_file_path
        app.logger.info(f'Processing attach_picture request is OK, new file: {new_file_path}')
        return make_response(response, 201)

    """
    Method to upload several files
    """
    @classmethod
    def get_upload_zip_file_response(cls, app, file):
        app.logger.debug(f'Processing Zip File: {file.filename}')
        file_like_object = file.stream._file  # get the input stream of the file
        zipfile_ob = zipfile.ZipFile(file_like_object)
        file_names = zipfile_ob.namelist()
        file_names = [file_name for file_name in file_names
                      if MicroUtils.allowed_file(file_name) and not file_name.startswith(MAC_AUTO_GENERATED_FILES)]
        saved_files = []
        if not file_names:
            app.logger.error('Error while attach_picture request. The file is not present inside zip file')
            raise InvalidUsage(ERROR_ZIP_FILE_RESPONSE, status_code=400)

        for file in file_names:
            zipfile_ob.extract(file, path=app.config['UPLOAD_FOLDER'])
            new_file_name = MicroUtils.generate_random_filename(file.rsplit('.', 1)[1].lower())
            upload_folder = app.config['UPLOAD_FOLDER']
            shutil.move(f'{upload_folder}/{file}', f'{upload_folder}/{new_file_name}')
            saved_files.append(new_file_name)
        response = GENERATED_FILE_RESPONSE
        response['path'] = saved_files
        return response

    """
    Method to store the image and return the generated link
    """
    @classmethod
    def save_image_and_get_link(cls, app, file):
        try:
            filename = MicroUtils.generate_random_filename(file.filename.rsplit('.', 1)[1].lower())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.logger.debug(f'Successfully stored {filename} file')
            new_file_path = f'/uploaded/{filename}'
        except Exception as e:
            app.logger.error(f'An error ocurred while saving file', e)
            raise InternalErrorUsage(ERROR_RESPONSE, 500)
        return new_file_path

