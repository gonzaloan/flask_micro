# Constants to be used in our app


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
UPLOAD_FOLDER = './uploaded'


# API Responses
ERROR_FILE_RESPONSE = {'response': 'Please attach a file', 'status': 400}
INVALID_FILE_RESPONSE = {'response': 'File is invalid or is not inside allowed extensions.', 'status': 400}
ERROR_RESPONSE = {'response': 'An error happened while storing image', 'status': 500}

GENERATED_FILE_RESPONSE = {'response': 'file uploaded successfully.', 'path': '', 'status': 201}
