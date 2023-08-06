"""
Wrapper exceptions
"""

class BaseException(Exception):
    def __init__(self):
        super().__init__()

class APIError(BaseException):
    def __init__(self, error=None, status=None, message=None):
        super().__init__()
        self.error = error
        self.status = status
        self.message = message



class APITimeoutError(APIError):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class APIClientResponseError(APIError):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

