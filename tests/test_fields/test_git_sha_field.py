from pytest import raises
from mjolk.parameter_exceptions import InvalidParameterException

from mjolk.fields.git_sha_field import GitShaField


def test_parameter_validators_sha_field_valid_sha():
    expected = GitShaField().validate(
        '1c81bb510335c461fa4d31f8245507ccfb7c7ae3')
    actual = '1c81bb510335c461fa4d31f8245507ccfb7c7ae3'

    assert expected == actual


def test_parameter_validators_sha_field_valid_sha_only_alpha():
    expected = GitShaField().validate(
        'acbdfeaccbfdfbebfdacbefdbdaceacdbfdbacdb')
    actual = 'acbdfeaccbfdfbebfdacbefdbdaceacdbfdbacdb'

    assert expected == actual


def test_parameter_validators_sha_field_invalid_sha_only_digits():
    expected = GitShaField().validate(
        '2398052789243758923768904532768590420704')
    actual = '2398052789243758923768904532768590420704'

    assert expected == actual


def test_parameter_validators_sha_field_too_short():
    with raises(InvalidParameterException) as exception:
        GitShaField().validate('1c81bb510335c461fa4d31f8245507ccfb7c7ae')

    assert exception.match(
        "The Git SHA '1c81bb510335c461fa4d31f8245507ccfb7c7ae' is malformed.")


def test_parameter_validators_sha_field_too_long():
    with raises(InvalidParameterException) as exception:
        GitShaField().validate('1c81bb510335c461fa4d31f8245507ccfb7c7ae34')

    assert exception.match(
        "The Git SHA '1c81bb510335c461fa4d31f8245507ccfb7c7ae34' is malformed.")


def test_parameter_validators_sha_field():
    with raises(InvalidParameterException) as exception:
        GitShaField().validate('master')

    assert exception.match("The Git SHA 'master' is malformed.")


def test_parameter_validators_sha_field_invalid_characters():
    with raises(InvalidParameterException) as exception:
        GitShaField().validate('1g81bb510335c461fa4d31f8245507ccfb7c7ae3')

    assert exception.match(
        "The Git SHA '1g81bb510335c461fa4d31f8245507ccfb7c7ae3' is malformed.")
