class ApiException(Exception):
    status_code = 500

    def __init__(self, message):
        super(ApiException, self).__init__()

        self.message = message

    def to_dict(self):
        rv = dict(code=self.status_code, message=self.message)
        return rv


class PlatformNotFoundException(ApiException):
    status_code = 404

    def __init__(self, message='Invalid platform parameter'):
        super(PlatformNotFoundException, self).__init__(message=message)


class InvalidSemverException(ApiException):
    status_code = 404

    def __init__(self, message='Invalid semver range'):
        super(InvalidSemverException, self).__init__(message=message)
