# Constants to be used in our app


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'zip']
UPLOAD_FOLDER = './uploaded'
MAC_AUTO_GENERATED_FILES = '__MACOSX'

# API Responses
ERROR_FILE_RESPONSE = {'response': 'Please attach a file', 'status': 400}
ERROR_ZIP_FILE_RESPONSE = {'response': 'Zip file does not contain valid image files', 'status': 400}
INVALID_FILE_RESPONSE = {'response': 'File is invalid or is not inside allowed extensions.', 'status': 400}
ERROR_RESPONSE = {'response': 'An error happened while storing image', 'status': 500}

GENERATED_FILE_RESPONSE = {'response': 'file(s) uploaded successfully.', 'path': '', 'status': 201}
