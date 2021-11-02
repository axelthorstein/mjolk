from pytest import fixture
from flask import Flask
from flask import jsonify

from mjolk.parameter_exceptions import ParameterException

app = Flask(__name__)  # pylint: disable=global-variable,invalid-name


@app.errorhandler(ParameterException)
def parameter_exception(error):  # pylint: disable=unused-variable
    """Return a parameter exception message.

    Args:
        error (str): The error.

    Returns:
        str: The formatted error message.
    """
    return jsonify(code=400, message=str(error)), 400


@fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client
