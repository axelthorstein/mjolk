from pytest import raises
from mjolk.parameter_exceptions import InvalidParameterException
from mjolk.parameter_exceptions import MissingParameterException

from mjolk.fields.azkaban_project_field import AzkabanProjectField


def test_parameter_validators_project_field_valid_name():
    expected = AzkabanProjectField().validate('test_project')
    actual = 'test_project'

    assert expected == actual


def test_parameter_validators_project_field_valid_name_with_caps():
    expected = AzkabanProjectField().validate('Test_project')
    actual = 'Test_project'

    assert expected == actual


def test_parameter_validators_project_field_valid_name_all_caps():
    expected = AzkabanProjectField().validate('TEST_PROJECT')
    actual = 'TEST_PROJECT'

    assert expected == actual


def test_parameter_validators_project_field_valid_name_multi_word():
    expected = AzkabanProjectField().validate('TestProject')
    actual = 'TestProject'

    assert expected == actual


def test_parameter_validators_project_field_valid_name_with_digits_and_symbols(
):
    expected = AzkabanProjectField().validate('Test_Project-Experiment')
    actual = 'Test_Project-Experiment'

    assert expected == actual


def test_parameter_validators_project_field_invalid_character():
    with raises(InvalidParameterException) as exception:
        AzkabanProjectField().validate('Longboat.Staging')

    assert exception.match(
        "Project names must start with a letter, followed by any number of letters, digits, '-' or '_'."
    )


def test_parameter_validators_project_field_invalid_first_character():
    with raises(InvalidParameterException) as exception:
        AzkabanProjectField().validate('1LongboatStaging')

    assert exception.match(
        "Project names must start with a letter, followed by any number of letters, digits, '-' or '_'."
    )


def test_parameter_validators_project_field_empty_string():
    with raises(MissingParameterException) as exception:
        AzkabanProjectField().validate('')

    assert exception.match("The 'azkaban_project' field must be supplied.")
