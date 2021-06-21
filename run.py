from flask import Flask, request, send_from_directory

from exceptions.exceptions import InvalidUsage, InternalErrorUsage
from services.image_service import ImagesService
from utils.constants import UPLOAD_FOLDER
from utils.utils import MicroUtils

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
image_service = ImagesService()


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return error.to_dict(), error.status_code


@app.errorhandler(InternalErrorUsage)
def handle_internal_error_usage(error):
    return error.to_dict(), error.status_code


@app.route('/attach', methods=['POST'])
def attach_picture():
    app.logger.info('Processing attach_picture request')
    MicroUtils.validate_if_empty_file_body(request.files, app)
    return image_service.attach_image(request.files['file'], app)


@app.route('/uploaded/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
