class AppException(Exception):
    """Base application exception."""
    pass


class DatabaseException(AppException):
    """Database related exception."""
    pass


class AuthenticationException(AppException):
    """Authentication related exception."""
    pass


class AuthorizationException(AppException):
    """Authorization related exception."""
    pass


class ValidationException(AppException):
    """Validation related exception."""
    pass