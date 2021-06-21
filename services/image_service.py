
"""
Class to abstract the service layer of the application to keep controller layer simplified.
"""
from flask import make_response
from exceptions.exceptions import InvalidUsage, InternalErrorUsage
from utils.constants import INVALID_FILE_RESPONSE, ERROR_RESPONSE, GENERATED_FILE_RESPONSE, MAC_AUTO_GENERATED_FILES, \
    ERROR_ZIP_FILE_RESPONSE, ERROR_RESIZING_RESPONSE, THUMBNAIL_EXPECTED_SIZE, THUMBNAIL_32_SIZE, THUMBNAIL_64_SIZE
from utils.utils import MicroUtils
import os
import zipfile
import shutil
from PIL import Image


class ImagesService:

    @classmethod
    def attach_image(cls, file, app):
        app.logger.debug(f'Processing inside Images Service file: {file.filename}')
        cls.validate_file_valid_extension(app, file)
        if MicroUtils.is_zip_file(file.filename):
            images_path = cls.save_image_and_get_link_from_zip(app, file)
        else:
            images_path = cls.save_image_and_get_link(app, file)
        modified_images = cls.generate_modified_thumnails(app, images_path)
        response = GENERATED_FILE_RESPONSE
        response['path'] = modified_images
        app.logger.info(f'Processing attach_picture request is OK, new file: {images_path}')
        return make_response(response, 201)

    @classmethod
    def generate_modified_thumnails(cls, app, images_path):
        modified_images = []
        try:
            for image in images_path:
                img = Image.open(f'uploaded/{image}')
                width, height = img.size
                if width >= THUMBNAIL_EXPECTED_SIZE[0] and height >= THUMBNAIL_EXPECTED_SIZE[1]:
                    app.logger.info(f'Image {image} will be resized. ')
                    img.thumbnail(THUMBNAIL_64_SIZE, Image.ANTIALIAS)
                    image_32 = f'uploaded/32x32_{image}'
                    image_64 = f'uploaded/64x64_{image}'
                    img.save(image_64, "PNG")
                    img.thumbnail(THUMBNAIL_32_SIZE, Image.ANTIALIAS)
                    img.save(image_32, "PNG")
                    modified_images.append(image_32)
                    modified_images.append(image_64)
                    # Lets remove original image
                    os.remove(f'uploaded/{image}')
                else:
                    app.logger.info(f'Image {image} will NOT be resized. ')
                    modified_images.append(image)

        except IOError as e:
            app.logger.error('An error happened while resizing photo: ', e)
            raise InternalErrorUsage(ERROR_RESIZING_RESPONSE, 500)
        return modified_images

    """
    Method to upload several files
    """
    @classmethod
    def save_image_and_get_link_from_zip(cls, app, file):
        app.logger.debug(f'Processing Zip File: {file.filename}')
        file_like_object = file.stream._file  # get the input stream of the file
        zipfile_ob = zipfile.ZipFile(file_like_object)
        file_names = zipfile_ob.namelist()
        file_names = [file_name for file_name in file_names
                      if MicroUtils.allowed_file(file_name) and not file_name.startswith(MAC_AUTO_GENERATED_FILES)]
        saved_files = []
        cls.validate_zip_file_without_valid_images(app, file_names)
        for file in file_names:
            zipfile_ob.extract(file, path=app.config['UPLOAD_FOLDER'])
            new_file_name = MicroUtils.generate_random_filename(file.rsplit('.', 1)[1].lower())
            upload_folder = app.config['UPLOAD_FOLDER']
            shutil.move(f'{upload_folder}/{file}', f'{upload_folder}/{new_file_name}')
            saved_files.append(new_file_name)
        return saved_files

    """
    Method to store the image and return the generated link
    """
    @classmethod
    def save_image_and_get_link(cls, app, file):
        try:
            filename = MicroUtils.generate_random_filename(file.filename.rsplit('.', 1)[1].lower())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.logger.debug(f'Successfully stored {filename} file')
            #new_file_path = f'uploaded/{filename}'
        except Exception as e:
            app.logger.error(f'An error ocurred while saving file', e)
            raise InternalErrorUsage(ERROR_RESPONSE, 500)
        return [filename]

    @classmethod
    def validate_file_valid_extension(cls, app, file):
        if file.filename == '' or not MicroUtils.allowed_file(file.filename):
            app.logger.error('Error while attach_picture request. The file is not valid')
            raise InvalidUsage(INVALID_FILE_RESPONSE, status_code=400)

    @classmethod
    def validate_zip_file_without_valid_images(cls, app, file_names):
        if not file_names:
            app.logger.error('Error while attach_picture request. The file is not present inside zip file')
            raise InvalidUsage(ERROR_ZIP_FILE_RESPONSE, status_code=400)