from flask import Flask, request, make_response, send_from_directory

from services.image_service import ImagesService
from utils.constants import UPLOAD_FOLDER, ERROR_FILE_RESPONSE

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
image_service = ImagesService()


@app.route('/attach', methods=['POST'])
def attach_picture():
    app.logger.info('Processing attach_picture request')
    if 'file' not in request.files:
        app.logger.error('Error while attach_picture request. The file is not present')
        return make_response(ERROR_FILE_RESPONSE, 400)
    file = request.files['file']
    return image_service.attach_image(file, app)


@app.route('/uploaded/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
