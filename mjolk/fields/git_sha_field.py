import re

from mjolk.parameter_exceptions import InvalidParameterException
from mjolk.fields.base_field import BaseField


class GitShaField(BaseField):

    def name(self):  # pylint: disable=no-self-use
        """Return the default parameter name.

        Returns:
            str: The default parameter name.
        """
        return 'sha'

    def validate_value(self, value):  # pylint: disable=no-self-use
        """Check that the value is a valid Git SHA.

        Args:
            value (str): A user inputted 64 character Git SHA.

        Returns:
            str: A valid Git SHA.

        Raises:
            InvalidParameterException: If the Git SHA is not valid.
        """
        if re.match(r'^\s*([0-9a-f]{40})$', value):
            return value

        raise InvalidParameterException(f"The Git SHA '{value}' is malformed.")
