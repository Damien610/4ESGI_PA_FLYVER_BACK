class CustomException(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code

class NotFound(CustomException):
    def __init__(self, detail: str = "Not found"):
        super().__init__(detail, 404)

class AlreadyExist(CustomException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(detail, 409)

class BadRequest(CustomException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(detail, 409)

class NotAuthorized(CustomException):
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(detail, 403)

class UnexpectedException(CustomException):
    def __init__(self, message: str):
        super().__init__(f"Unexpected error: {message}", status_code=500)