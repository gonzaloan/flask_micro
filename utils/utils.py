from utils.constants import ALLOWED_EXTENSIONS
import random
import string
"""
This is a utils class for every utility that can be used across the service.
"""


class MicroUtils:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def generate_random_filename(extension):
        """This method will generate a random 15 letters string value to assign to every uploaded picture"""
        letters = string.ascii_lowercase
        random_name = ''.join(random.choice(letters) for i in range(15))
        return f'{random_name}.{extension}'
