from mjolk.parameter_exceptions import MissingParameterException


class BaseField:

    def __init__(self, name=None, default=None):
        self.name = name or self.name()
        self.default = default

    def name(self):  # pylint: disable=no-self-use
        pass

    def validate_value(self):
        pass

    def validate(self, value):
        """Check that the value is a valid.

        Args:
            value (str): A user inputted value.

        Returns:
            str: A validated value.

        Raises:
            MissingParameterException: If the value and default are not set.
        """
        if not value and self.default:
            return self.default
        elif not value:
            raise MissingParameterException(
                f"The '{self.name}' field must be supplied.")

        return self.validate_value(value)
