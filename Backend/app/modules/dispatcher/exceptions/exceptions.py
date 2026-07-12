from fastapi import status
from app.auth.exceptions.exceptions import AuthException

class DispatcherException(AuthException):
    def __init__(self, message: str, error_code: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message=message, error_code=error_code, status_code=status_code)
