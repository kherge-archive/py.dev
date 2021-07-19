from dev.common import LABEL_NAME, NotManaged, is_managed
from unittest import TestCase, mock

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
