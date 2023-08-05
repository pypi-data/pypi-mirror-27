# coding=utf-8
from __future__ import unicode_literals

import inspect

from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from .errors import ExtensibleValidationError


class CleanMixin(object):
    @cached_property
    def validations(self):
        return ValidationManager(self)

    def clean(self):
        self.validations()


class ValidationManager(object):
    def __init__(self, model, clean_methods=None):
        self.errors = []
        self.model = model
        self.clean_methods = clean_methods or [method for method in dir(model) if method.startswith('clean_') and callable(getattr(model, method))]

    def __call__(self):
        self.full_clean()

    def full_clean(self):
        self.errors = []
        self.collect_validation_errors()
        if self.errors:
            raise ExtensibleValidationError(self.errors)

    def collect_validation_errors(self):
        for name in self.clean_methods:
            method = getattr(self.model, name)
            try:
                if inspect.isgeneratorfunction(method):
                    self.errors.extend(method())
                else:
                    error = method()
                    if isinstance(error, ValidationError):
                        self.append_error(error, name)
            except ValidationError as ex:
                self.append_error(ex, name)

    def append_error(self, error, clean_name):
        if not hasattr(error, 'error_dict'):
            field_name = self.get_field_name(clean_name)
            error = ValidationError({field_name: error})
        self.errors.append(error)

    # noinspection PyMethodMayBeStatic
    def get_field_name(self, clean_name):
        field_name = clean_name.replace('clean_', '')
        return field_name
