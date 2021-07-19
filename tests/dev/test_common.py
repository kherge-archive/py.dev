from dev.common import LABEL_NAME, NotManaged, get_docker, is_managed
from unittest import TestCase, mock

def test_get_docker_with():
    expected = {}
    actual = get_docker(expected)

    assert expected == actual

@mock.patch('docker.from_env')
def test_get_docker_without(mock_from_env: mock.Mock):
    expected = {}

    mock_from_env.return_value = expected

    actual = get_docker(None)

    assert expected == actual

def test_is_managed_false():
    obj = mock.MagicMock()
    obj.labels = {}

    assert is_managed(obj) == False

def test_is_managed_true():
    obj = mock.MagicMock()
    obj.labels = {
        LABEL_NAME: "true"
    }

    assert is_managed(obj) == True

class TestNotManaged(TestCase):

    def test_init(self):
        error = NotManaged('type', 'name')

        assert error.name == 'name'
        assert error.type == 'type'
