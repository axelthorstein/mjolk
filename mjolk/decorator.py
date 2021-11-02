from functools import wraps
from flask import request
from flask import jsonify

from mjolk.validator import Validator


def validate(*fields):
    """Validate the POSTed Flask request data.

    Note: The endpoint function needed to be decorated twice in order for the
    field classes to be passed in intuitively.

    Args:
        fields List[Field]: The list of fields to validate.

    Returns:
        Function: The decorated endpoint decorator.
    """

    def wrap(func):
        """Wrap the endpoint function with a validation decorator.

        Args:
            func (Function): The endpoint function that is being decorated.

        Returns:
            Function: Invokes and returns the value of the decorated function.
        """

        @wraps(func)
        def decorator():
            """Call the field validators on the POSTed data.

            Returns:
                dict: The successful JSON response.
            """
            data = dict(request.form)
            validated_parameters = Validator(func, fields).validate(data)

            return jsonify(code=200, message=func(**validated_parameters)), 200

        return decorator

    return wrap
