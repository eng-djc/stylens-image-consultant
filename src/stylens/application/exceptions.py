"""Application-layer errors translated by the HTTP adapter."""


class SessionNotFoundError(LookupError):
    pass


class ConsentRequiredError(PermissionError):
    pass


class InvalidImageError(ValueError):
    pass

