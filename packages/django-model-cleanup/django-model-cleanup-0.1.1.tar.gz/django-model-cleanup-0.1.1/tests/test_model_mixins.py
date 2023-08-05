# coding=utf-8

from django.core.exceptions import ValidationError

from tests.app import models


def test_model_has_validations():
    item = models.SomeModel()
    assert hasattr(item, "validations")


def test_model_errors():
    item = models.SomeModel()
    try:
        item.full_clean()
    except ValidationError as ex:
        assert ex.message_dict == {
            'bar': ['Bar is wrong cause 2 > 1!', 'Bar legacy error 7 > 5!'],
            'foo': ['Foo is bad'],
        }
