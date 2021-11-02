from pytest import raises

from mjolk.fields.base_field import BaseField
from mjolk.validator import Validator
from mjolk.parameter_exceptions import InvalidParameterException
from mjolk.parameter_exceptions import UnrecognizedParameterException


class Field(BaseField):

    def name(self):  # pylint: disable=no-self-use
        return 'field'

    def validate_value(self, value):  # pylint: disable=no-self-use
        if value == 'value':
            return value

        raise InvalidParameterException('The value is not valid.')


def endpoint(field):  # pylint: disable=unused-argument
    pass


def no_validate_endpoint(field, no_validate_field):  # pylint: disable=unused-argument
    pass


def test_validator_valid_field():
    data = {'field': ['value']}

    expected = {'field': 'value'}
    actual = Validator(endpoint, [Field()]).validate(data)

    assert expected == actual


def test_validator_valid_fields_no_fields_to_validate():
    data = {'field': ['value'], 'no_validate_field': ['no_validate_value']}

    expected = {'field': 'value', 'no_validate_field': 'no_validate_value'}
    actual = Validator(no_validate_endpoint, [Field()]).validate(data)

    assert expected == actual


def test_validator_valid_field_with_default():
    data = {'field': []}

    expected = {'field': 'default_value'}
    actual = Validator(
        endpoint, [Field(default='default_value')]).validate(data)

    assert expected == actual


def test_validator_valid_field_no_validation():
    data = {'field': ['value']}

    expected = {'field': 'value'}
    actual = Validator(endpoint, []).validate(data)

    assert expected == actual


def test_validator_get_function_paramters():
    expected = ['field']
    actual = Validator.get_function_parameters(endpoint)

    assert expected == actual


def test_validator_get_function_paramters_multiple_params():
    expected = ['field', 'no_validate_field']
    actual = Validator.get_function_parameters(no_validate_endpoint)

    assert expected == actual


def test_validator_delist_dict_value_in_list():
    data = {'field': ['value']}

    expected = {'field': 'value'}
    actual = Validator.delist_dict(data)

    assert expected == actual


def test_validator_delist_dict_value_not_in_list():
    data = {'field': 'value'}

    expected = {'field': 'value'}
    actual = Validator.delist_dict(data)

    assert expected == actual


def test_validator_delist_dict_no_values():
    data = {}

    expected = {}
    actual = Validator.delist_dict(data)

    assert expected == actual


def test_validator_too_many_parameters():
    data = {'field': ['value'], 'extra_field': ['extra_value']}

    with raises(UnrecognizedParameterException):
        Validator(endpoint, [Field()]).validate(data)


def test_validator_no_parameters():
    data = {}

    with raises(UnrecognizedParameterException):
        Validator(endpoint, [Field()]).validate(data)
