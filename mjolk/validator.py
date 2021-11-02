import inspect
from mjolk.parameter_exceptions import UnrecognizedParameterException


class Validator:

    def __init__(self, func, fields):
        self.fields = fields
        self.function_parameters = Validator.get_function_parameters(func)

    @staticmethod
    def get_function_parameters(func):
        """Return the list of expected function parameters.

        Args:
            func (Function): The function with parameters to be validated.

        Returns:
            dict: The list of expected function parameters.
        """
        return list(inspect.signature(func).parameters.keys())

    @staticmethod
    def delist_dict(data):
        """De-list the non validated HTTP parameters.

        Args:
            data (dict): The HTTP parameters.

        Returns:
            dict: The HTTP parameters.
        """
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        return data

    def apply(self, data):
        """Apply the field validators to the parameters.

        Args:
            data (dict): The HTTP parameters.

        Returns:
            dict: The HTTP parameters.
        """
        for field in self.fields:
            value = data.get(field.name)

            if value:
                data[field.name] = field.validate(*value)
            elif field.default:
                data[field.name] = field.default

        return Validator.delist_dict(data)

    def format_error_message(self, data):
        """Format an error message for unrecognized parameters.

        Args:
            data (dict): A dictionary of parameters.

        Returns:
            str: The an error message for a unrecognized parameters.
        """
        data = ', '.join(list(data))
        params = ', '.join(self.function_parameters)

        return (f"Unrecognized keyword arguments: [{data}]. " +
                f"Expected keyword arguments: [{params}].")

    def validate(self, unvalidated_parameters):
        """Validate the POSTed Flask request parameters.

        If any of the incoming named parameters match existing validator
        classes then they will validate that value and return the
        correct corresponding object if necessary.

        Args:
            unvalidated_parameters (dict): The user inputted parameters.

        Returns:
            dict: The validated user inputted parameters.

        Raises:
            UnrecognizedParameterException: If an unknown parameter was posted.
        """
        validated_parameters = self.apply(unvalidated_parameters)

        # Make sure the parameters match the endpoint function signature.
        if set(self.function_parameters) != set(validated_parameters):
            raise UnrecognizedParameterException(
                self.format_error_message(validated_parameters))

        return validated_parameters
