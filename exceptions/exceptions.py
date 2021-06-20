class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.error_message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {
            'message': self.error_message,
            'error': True,
        }


class InternalErrorUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=500):
        Exception.__init__(self)
        self.error_message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {
            'message': self.error_message,
            'error': True,
        }