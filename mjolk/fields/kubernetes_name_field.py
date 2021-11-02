import re

from mjolk.parameter_exceptions import InvalidParameterException
from mjolk.fields.base_field import BaseField


class KubernetesNameField(BaseField):

    def name(self):  # pylint: disable=no-self-use
        """Return the default parameter name.

        Returns:
            str: The default parameter name.
        """
        return 'kubernetes_name'

    def validate_value(self, value):  # pylint: disable=no-self-use
        """Check that the value is a valid Kubernetes name.

        Args:
            value (str): A user inputted name.

        Returns:
            str: A valid name with only lowercase, dashes, and dots.

        Raises:
            InvalidParameterException: If the name is not valid.
        """
        if re.match(r'[a-z0-9-.]{1,253}$', value):
            return value

        raise InvalidParameterException(
            f"The value '{value}' must be under 253 characters and " +
            "consist of lower case alphanumeric characters, -, and .")
