import re

from mjolk.parameter_exceptions import InvalidParameterException
from mjolk.fields.base_field import BaseField


class AzkabanProjectField(BaseField):

    def name(self):  # pylint: disable=no-self-use
        """Return the default parameter name.

        Returns:
            str: The default parameter name.
        """
        return 'azkaban_project'

    def validate_value(self, value):  # pylint: disable=no-self-use
        """Check that the value is a valid azkaban project name.

        Args:
            value (str): A user inputted azkaban project name.

        Returns:
            Class: A valid azkaban project name class.

        Raises:
            InvalidParameterException: If the azkaban project name is not valid.
        """
        if re.match(r'^(?!.*\/\/)[A-Za-z][A-Za-z0-9_-]*$', value):
            return value

        raise InvalidParameterException(
            "Project names must start with a letter, followed by any number " +
            "of letters, digits, '-' or '_'.")
