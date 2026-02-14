class AppException(Exception):
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ConflictException(AppException):
    status_code = 409


class UnauthorizedException(AppException):
    status_code = 401


class ForbiddenException(AppException):
    status_code = 403


class NotFoundException(AppException):
    status_code = 404