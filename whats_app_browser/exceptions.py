from starlette import status


class NoSuchProfile(Exception):
    _STATUS_CODE = status.HTTP_404_NOT_FOUND


class NoProfilePicture(Exception):
    _STATUS_CODE = status.HTTP_404_NOT_FOUND


class NotAuthenticated(Exception):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
