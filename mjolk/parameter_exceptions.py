class ParameterException(Exception):
    """General parameter exception"""
    pass


class InvalidParameterException(ParameterException):
    """Exception for field validation violations."""
    pass


class MissingParameterException(ParameterException):
    """Exception for missing expected parameter."""
    pass


class UnrecognizedParameterException(ParameterException):
    """Exception for unrecognized parameters."""
    pass
