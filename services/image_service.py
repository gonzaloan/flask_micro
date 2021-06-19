
"""
Class to abstract the service layer of the application to keep controller layer simplified.
"""
from requests import get

from flask import make_response, url_for

from utils.constants import INVALID_FILE_RESPONSE, ERROR_RESPONSE, GENERATED_FILE_RESPONSE
from utils.utils import MicroUtils
import os


class ImagesService:

    @classmethod
    def attach_image(cls, file, app):
        app.logger.debug(f'Processing inside Images Service file: {file.filename}')
        if file.filename == '' or not MicroUtils.allowed_file(file.filename):
            return make_response(INVALID_FILE_RESPONSE, 400)

        try:
            filename = MicroUtils.generate_random_filename(file.filename.rsplit('.', 1)[1].lower())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.logger.debug(f'Successfully stored {filename} file')

        except Exception as e:
            app.logger.error(f'An error ocurred while saving file', e)
            return make_response(ERROR_RESPONSE, 500)

        new_file_path = f'/uploaded/{filename}'
        response = GENERATED_FILE_RESPONSE
        response['path'] = new_file_path
        app.logger.info(f'Processing attach_picture request is OK, new file: {new_file_path}')
        return make_response(response, 201)

