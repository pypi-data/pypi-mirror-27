#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `django-model-cleanup` package."""
from __future__ import unicode_literals

import pytest
from django.db.models.fields.related import ForeignKey
from django.forms.utils import ErrorDict, ErrorList
from django.utils import translation
from django.utils.translation import override

from django_model_cleanup.errors import ExtensibleValidationError as ValidationError

# This will be formatted differently on py27
EN_MESSAGE = "Foo instance with Bar %r does not exist." % 'Baz'
PL_MESSAGE = "Foo z polem Bar o wartości %r nie istnieje." % 'Baz'
FR_MESSAGE = "L'instance Foo avec %r dans Bar n'existe pas." % 'Baz'


def test_init_with_string():
    # Start simple
    v = ValidationError('A bad value here!')
    assert v.messages == ['A bad value here!']
    assert v.error_list == [v]
    assert hasattr(v, 'error_dict') is False


def test_init_with_string_and_params():
    # Add formatting
    message, params = 'Not correct %d!=%d %s!', (1, 2, 'bam!')
    v = ValidationError(message, params=params)
    assert v.messages == ['Not correct 1!=2 bam!!']
    assert v.error_list == [v]
    assert v.message == message
    assert v.params == params


def test_init_with_dict():
    # dict will trigger recursive init of multiple ValidationErrors
    v = ValidationError({'field': 'A test error message'})
    # will have special attribute
    assert hasattr(v, 'error_dict')
    error = v.error_dict

    # it will mimic original dict
    assert 'field' in error
    field_errors = error['field']

    # but instead of single error we'll have a list
    assert isinstance(field_errors, list)
    assert isinstance(field_errors[0], ValidationError)

    # where we'll have a list errors again
    assert field_errors[0].messages == ['A test error message']
    # this error_list is a one element list of [self]
    assert field_errors[0].error_list == [field_errors[0]]

    # all this will be flattened with messages property
    assert v.messages == ['A test error message']


def test_init_with_string_list():
    messages = ['Error A', 'Error B']
    v = ValidationError(messages)
    # no error_dict
    assert hasattr(v, 'error_dict') is False

    # but messages are here
    assert v.messages == messages

    # and we have error_list
    assert hasattr(v, 'error_list')
    assert isinstance(v.error_list, list)

    # which has 2 elements, as an initial string list
    assert isinstance(v.error_list[0], ValidationError)
    assert isinstance(v.error_list[1], ValidationError)

    # which in turn have both a one element of list of error message
    assert v.error_list[0].messages == ['Error A']
    assert v.error_list[1].messages == ['Error B']

    # And they contain itself in error_list
    assert v.error_list[0].error_list == [v.error_list[0]]
    assert v.error_list[1].error_list == [v.error_list[1]]


def test_init_with_dict_and_params():
    v = ValidationError({'field': 'Not true: %s>%s'}, params=(1, 2))
    # Sorry params do not work with dict
    assert v.messages == ['Not true: 1>2']
    # DONE: Make sure params work with dict initialization

    # to overcome this we need to pass a validation error instance
    inner = ValidationError('Not true: %s>%s', params=(1, 2))
    v = ValidationError({'field': inner})
    # Sorry params do not work with dict
    assert v.messages == ['Not true: 1>2']
    # this is hack'y
    # but we still have an error dict, few!
    assert v.error_dict == {'field': [inner]}


def test_init_with_list_and_params():
    v = ValidationError(['Not true: %s>%s', 'Yep, still wrong %s>%s'], params=(1, 2))
    # params work with list
    assert v.messages == ['Not true: 1>2', 'Yep, still wrong 1>2']
    # DONE: Make sure params work with list initialization


@pytest.fixture
def polish_language(settings):
    settings.LANGUAGE_CODE = 'pl'


def get_translated_validation_error(**kwargs):
    """We'll use some internal django message that is supposed to be translated"""
    message = ForeignKey.default_error_messages['invalid']
    params = {'model': 'Foo', 'field': 'Bar', 'value': 'Baz'}
    params.update(kwargs)
    return ValidationError(message, params=params)


def test_init_with_translated_text(polish_language):
    # Add formatting and language
    v = get_translated_validation_error()
    # when asked for message will be translated
    assert v.messages == [PL_MESSAGE]
    # but is stored as lazy object
    assert v.message.__class__.__name__ == '__proxy__'
    # so changing the language is no problem
    with translation.override('fr'):
        assert v.messages == [FR_MESSAGE]


def test_init_with_dict_and_params_and_translation(polish_language):
    v = get_translated_validation_error()

    # Params encapsulation still works with translated strings. Cool.
    v = ValidationError({'some_field': v})
    # when asked for message will be translated
    assert v.messages == [PL_MESSAGE]
    assert v.message_dict == {'some_field': [PL_MESSAGE]}

    # is still stored as lazy object
    assert v.error_dict['some_field'][0].message.__class__.__name__ == '__proxy__'

    # and changing the language has still a desired effect
    with translation.override('fr'):
        assert v.messages == [FR_MESSAGE]
        assert v.message_dict == {'some_field': [FR_MESSAGE]}


def test_concat_errors_simple():
    # you can't raise multiple validation exceptions
    # and giving them to user one after another is a bad UX
    # so we would like to concat them, passing a list to init works
    v1 = ValidationError('foo')
    v2 = ValidationError('bar')
    error = ValidationError([v1, v2])
    assert error.messages == ['foo', 'bar']


def test_concat_errors_with_field_keys():
    # but want if want to concat errors indicating a field?
    v1 = ValidationError({'a': 'foo'})
    v2 = ValidationError({'b': 'bar'})
    error = ValidationError([v1, v2])
    assert error.messages == ['foo', 'bar']
    # in this version error dict is here
    assert hasattr(error, 'error_dict')
    # DONE: Preserve error_dict {field: messages} with concatenations
    assert error.message_dict == {'a': ['foo'], 'b': ['bar']}


def test_concat_errors_with_field_and_params():
    # so what about params?
    v1 = ValidationError({'field': 'Not true: %s>%s'}, params=(1, 2))
    v2 = ValidationError({'field': 'Also Not true: %s>%s'}, params=(1, 3))
    error = ValidationError([v1, v2])
    # our version remembers params so string formatting works!
    assert error.messages == ['Not true: 1>2', 'Also Not true: 1>3']

    # but there was a hack
    v1 = ValidationError('Not true: %s>%s', params=(1, 2))
    v2 = ValidationError('Also Not true: %s>%s', params=(1, 3))
    v1 = ValidationError({'field': v1})
    v2 = ValidationError({'field': v2})
    error = ValidationError([v1, v2])
    # yay, it still works
    assert error.messages == ['Not true: 1>2', 'Also Not true: 1>3']
    # and in this version error dict is present
    assert error.message_dict == {'field': ['Not true: 1>2', 'Also Not true: 1>3']}


def test_concat_translated_errors(polish_language):
    # lets try concat error with translated text
    v = get_translated_validation_error()
    error = ValidationError([v])

    # yay, works
    assert error.messages == [PL_MESSAGE]
    translation.activate('fr')
    assert error.messages == [FR_MESSAGE]


def test_concat_translated_errors_and_fields(polish_language):
    # lets try concat error with translated text
    v = get_translated_validation_error()
    v = ValidationError({'boo': v})
    error = ValidationError([v])

    # yup, still works
    assert error.messages == [PL_MESSAGE]
    translation.activate('fr')
    assert error.messages == [FR_MESSAGE]
    assert error.message_dict == {'boo': [FR_MESSAGE]}


def test_forms_error_dict():
    # the ultimate end game is to show these to the user
    # django wraps validation errors with ErrorDict consisting of ErrorList's
    # this is done in the BaseModelForm._post_clean method
    # which in turn calls _update_error that overrides message text if needed
    # and calls add_error with a single ValidationError instance
    # which must have an error_dict
    # TODO: Final ValidationError must have an error_dict with __all__ where field as originally missing
    # for each field and __all__ a ErrorList instance will be created
    # and extended with ValidationError instance error_list for given key.

    v = get_translated_validation_error()
    v = ValidationError({'boo': v, 'zap': [ValidationError('An error here!'), ValidationError('Yet another one!')]})

    form_errors = ErrorDict()
    # lest simulate add_error here
    for field, errors in v.error_dict.items():
        form_field_errors = form_errors.setdefault(field, ErrorList())
        form_field_errors.extend(errors)

    assert form_errors == {'boo': [EN_MESSAGE], 'zap': ['An error here!', 'Yet another one!']}
    # Let's find out how language change will affect the result
    with override('fr'):
        assert form_errors == {'boo': [FR_MESSAGE], 'zap': ['An error here!', 'Yet another one!']}
