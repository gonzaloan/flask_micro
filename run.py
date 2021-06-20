from flask import Flask, request, make_response, send_from_directory

from exceptions.exceptions import InvalidUsage, InternalErrorUsage
from services.image_service import ImagesService
from utils.constants import UPLOAD_FOLDER, ERROR_FILE_RESPONSE

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
    if 'file' not in request.files:
        app.logger.error('Error while attach_picture request. The file is not present')
        raise InvalidUsage(ERROR_FILE_RESPONSE, status_code=400)

    file = request.files['file']
    return image_service.attach_image(file, app)


@app.route('/uploaded/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
