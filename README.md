# Mjólk

Mjolk is a simple library for validating POSTed data to Flask application endpoints.

The original motivation of this project was to extend and abstract validation capabilities of Flask applications that are used for APIs or non-web form projects. There are a number of basic fields defined for common parameters such as fixed lenth strings, Github SHAs, floats with a fixed decimal place, various date-time formats, and more. Mjolk also grants the ability to create custom fields to validate under any conditions, or to set default values. This was created with the hopes of providing a simple, elegant, and Pythonic interface for parameter validation.

Mjolk runs on Python 3.6.


## Motivation

There are alternatives that provide the essential functionality of this project, however the main objectives that Mjolk addresses that other libraries don't are as follows:
- Removes the bloat `try/catch`'s spread among multiple endpoints
- Separates the validation logic from the actual logic of the endpoint
- Makes the method of validation consistent and reusable
- Allows for a finer grained control over parameters on a per endpoint basis
- Executes before endpoint logic, providing quick feedback for invalid inputs


## Usage

### Basic Usage

The most basic usage is to simply apply the decorator to an endpoint with a single field validator implemented by the library. 

Important notes:
- All of the core field validator names must correspond with the parameter name without the `Field` suffix. So in this case `StringField` will validate data posted to the `string` keyword, and therefore accessible under the `string` variable name in the function. The name [can be overridden](#overriding-parameter-names)
- None of the core validators will have defaults, though [they can be set manually](#setting-default-values)
- The validation occurs after the Flask app is instantiated, but before any of the endpoint logic is executed
- All responses are returned as JSON with a status code

Example:
```python
from mjolk.validate import validate
from mjolk.fields.string_field import StringField

@app.route('/endpoint')
@validate(StringField())
def endpoint(string):
    return (string,)
```

Here is an example of data posted to this endpoint with a valid value:
```python
>>> data = {'string': 'valid_value'}
>>> request.post('mjolk.com/api/endpoint', data=data)
{"code": "200", "message": "('valid_value',)"}
```

### Custom Fields

One of the main features of Mjolk is the ability to define custom fields to validate incoming data.

Important notes:
- Two methods `name` and `validate_value` must be overridden.
- The name method defines what keyword the data must be posted to and the name of the parameter that will be accessible in the endpoint.
- It is highly recommended that a `ParameterException` is raised if the parameter does not meet the necessary conditions.
- The field class name should be suffixed with `Field` and must inherit from the `BaseField` class.
- If the value is valid, then it should be returned.

A custom field can be define as such:
```python
# Located in some custom field module in the project.
from mjolk.fields.base_field import BaseField
from mjolk.parameter_exceptions import InvalidParameterException


class SomeField(BaseField):

    def name(self):
        """Return the default parameter name.

        Returns:
            str: The default parameter name.
        """
        return 'field_name'

    def validate_value(self, value):
        """Check that the value is valid.

        Args:
            value (str): A user inputted value.

        Returns:
            str: A valid value.

        Raises:
            InvalidParameterException: If the value is not valid.
        """
        if matches_some_condition(value):
            return value

        raise InvalidParameterException(f"The parameter '{value}' is invalid.")
```

Here is an example of applying a custom field to be validated:
```python
from custom.field.module import SomeField

@app.route('/endpoint')
@validate(SomeField())
def endpoint(field_name):
    return (field_name,)
```

Here is an example of data posted to this endpoint with a valid value:
```python
>>> data = {'field_name': 'valid_value'}
>>> request.post('mjolk.com/api/endpoint', data=data)
{"code": "200", "message": "('valid_value',)"}
```


### Overriding Parameter Names

If there is a need to override the parameter name, for example if you want to use the same validator for two different parameters, then you can assign each field its `name` keyword parameter.

```python
@app.route('/endpoint')
@validate(SomeField(name='first_name'), SomeField(name='second_name'))
def endpoint(first_name, second_name):
    return (first_name, second_name)
```
Both parameters are validated under the same conditions, but they are accessible under different names.

Then they will require parameters under these keywords to be posted:
```python
>>> data = {'first_name': 'first_value', 'second_name': 'second_value'}
>>> request.post('mjolk.com/api/endpoint', data=data)
{"code": "200", "message": "('first_value', 'second_value')"}
```


### Setting Default Values

If there is a need to set a default for a parameter this can be done through the fields `default` keyword parameter. This allows any default value to be return in the case that the value is not supplied by the user. If the user supplies any value however the default will not be used. Any custom fields will also have this ability if they inherit from the `BaseField` class.

```python
@app.route('/endpoint')
@validate(SomeField(), SomeField(name='other_name', default='other_value'))
def endpoint(field_name, other_name):
    return (field_name, other_name)
```

Then if the keyword is not posted the default value will be used instead.
```python
>>> data = {'field_name': 'valid_value'}
>>> request.post('mjolk.com/api/endpoint', data=data)
{"code": "200", "message": "('valid_value', 'other_value')"}
```

### Invalid Parameters

If the value of a parameter is invald then the `ParameterException` will be thrown. Provided that [these exceptions are being caught and wrapped](#returning-invalid-responses-as-json), then they will return a message an appropriate JSON error object:
```python
>>> data = {'field_name': 'invalid_value'}
>>> request.post('mjolk.com/api/endpoint', data=data)
{"code": "400", "message": "The parameter 'invalid_value' is invalid."}
```


### Returning Invalid Responses as JSON

In order to make sure that all of the parameter exceptions are returned as JSON objects we can use Flasks application `errorhandler` method to catch any custom `ParameterException` and format the return message properly. Otherwise the exceptions will be raised normally and no response will be returned to the user.

Simply add this block to your project:
```python
from flask import jsonify
from mjolk.parameter_exceptions import ParameterException

@app.errorhandler(ParameterException)
def parameter_exception(error):
    """Return a parameter exception message.

    Args:
        error (str): The error.

    Returns:
        str: The formatted error message.
    """
    return jsonify(code=400, message=str(error)), 400
```

You can also add your own custom parameter exception by creating a subclass exception:
```python
from mjolk.parameter_exceptions import ParameterException

class CustomParameterException(ParameterException):
    """Exception for some custom case."""
    pass
```

### Compatibility with Blueprints

Mjolk is compatible with endpoints that are registered to Flask Blueprints, but the `@validate` must be below the Blueprint registration:
```python
BLUEPRINT = Blueprint('example', __name__)

@BLUEPRINT.route('/endpoint', methods=['POST'])
@validate(SomeField())
def endpoint(first_name):
    return (first_name,)
```


## Development

### Setup

Running `make all` will enter the shell into a `pipenv shell` which will create a virtual environment to work in. This will install the necessary production and development dependencies.


### Formatting

Mjolk follows somewhat strict guidelines on formatting, adhering to PEP8, custom Pylint rules, and [Google's yapf](https://github.com/google/yapf). Before committing any code it is advised to run:
```
make lint
```
and/or
```
make format
```


### Testing

To run the entire testing suite:
```
make test
```
Alternatively to run a single test file only:
```
make test tests/test_file.py
```
It is also possible to run a single test case by running:
```
make test tests/test_file.py::test_case
```

http://docs.python-eve.org/en/latest/index.html