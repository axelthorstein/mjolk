import json

from mjolk.decorator import validate
from mjolk.fields.git_sha_field import GitShaField


def test_set_up(client):

    @client.application.route('/test_endpoint', methods=['POST'])
    @validate(GitShaField(name='sha'))
    def test_endpoint(sha):  # pylint: disable=unused-variable
        return "validated_" + sha


def test_validate_on_function(client):
    data = {'sha': 'ee81358f199c0ea27d9e8960f32524c2f14331a0'}

    expected = {
        'code': 200,
        'message': 'validated_ee81358f199c0ea27d9e8960f32524c2f14331a0'
    }
    actual = json.loads(client.post('/test_endpoint', data=data).data)

    assert expected == actual


def test_validate_on_function_invalid_arg_name(client):
    data = {'shas': 'ee81358f199c0ea27d9e8960f32524c2f14331a0'}

    expected = {
        'code':
        400,
        'message':
        'Unrecognized keyword arguments: [shas]. Expected keyword arguments: [sha].'
    }
    actual = json.loads(client.post('/test_endpoint', data=data).data)

    assert expected == actual


def test_validate_on_function_extra_arg(client):
    data = {'sha': 'ee81358f199c0ea27d9e8960f32524c2f14331a0', 'name': 'test'}

    expected = {
        'code':
        400,
        'message':
        'Unrecognized keyword arguments: [sha, name]. Expected keyword arguments: [sha].'
    }
    actual = json.loads(client.post('/test_endpoint', data=data).data)

    assert expected == actual


def test_validate_on_function_no_args(client):
    data = {}

    expected = {
        'code':
        400,
        'message':
        'Unrecognized keyword arguments: []. Expected keyword arguments: [sha].'
    }
    actual = json.loads(client.post('/test_endpoint', data=data).data)

    assert expected == actual
