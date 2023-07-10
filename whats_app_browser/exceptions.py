from starlette import status


class NoSuchProfile(Exception):
    _STATUS_CODE = status.HTTP_404_NOT_FOUND

    def __init__(self, phone, message=None):
        message = message or f"Profile with phone {phone!r} not found!"
        super().__init__(message)


class NoProfilePicture(Exception):
    _STATUS_CODE = status.HTTP_404_NOT_FOUND

    def __init__(self, message=None):
        message = message or "Profile picture not found"
        super().__init__(message)


class NotAuthenticated(Exception):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message: str = "You are not authorized"):
        super().__init__(message)


class Authenticated(Exception):
    _STATUS_CODE = status.HTTP_403_FORBIDDEN

    def __init__(self, message: str = "You are already logged in"):
        super().__init__(message)
