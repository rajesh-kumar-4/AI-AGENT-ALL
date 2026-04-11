from fastapi import status


class AppException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "app_error"
    message = "An application error occurred."

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
        super().__init__(self.message)


class NotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"
    message = "Resource not found."


class InvalidDataException(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    code = "invalid_data"
    message = "The data provided is invalid."


class UnauthorizedException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "unauthorized"
    message = "Authentication failed."
