from pytest import raises
from mjolk.parameter_exceptions import InvalidParameterException
from mjolk.parameter_exceptions import MissingParameterException

from mjolk.fields.kubernetes_name_field import KubernetesNameField


def test_parameter_validators_kubernetes_name_field_valid_name():
    expected = KubernetesNameField().validate('test-pod.test')
    actual = 'test-pod.test'

    assert expected == actual


def test_parameter_validators_kubernetes_name_field_invalid_length():
    pod_name = (
        'test-pod-test-pod-test-pod-test-pod-test-pod-test-pod-test-pod-' +
        'test-pod-test-pod-test-pod-test-pod-test-pod-test-pod-test-pod-' +
        'test-pod-test-pod-test-pod-test-pod-test-pod-test-pod-test-pod-' +
        'test-pod-test-pod-test-pod-test-pod-test-pod-test-pod-test-pod-' +
        'test-pod-test-pod-test-pod-test-pod-test-pod-test-pod-test-pod-')

    with raises(InvalidParameterException) as exception:
        KubernetesNameField().validate(pod_name)

    assert exception.match(
        f"The value '{pod_name}' must be under 253 characters and consist of lower case alphanumeric characters, -, and ."
    )


def test_parameter_validators_kubernetes_name_field_invalid_characters():
    with raises(InvalidParameterException) as exception:
        KubernetesNameField().validate('test=pod')

    assert exception.match(
        "The value 'test=pod' must be under 253 characters and consist of lower case alphanumeric characters, -, and ."
    )


def test_parameter_validators_kubernetes_name_field_empty_string():
    with raises(MissingParameterException) as exception:
        KubernetesNameField().validate('')

    assert exception.match("The 'kubernetes_name' field must be supplied.")
