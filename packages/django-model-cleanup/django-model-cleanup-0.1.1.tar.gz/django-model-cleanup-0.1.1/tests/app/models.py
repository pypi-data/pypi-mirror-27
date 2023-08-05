# coding=utf-8
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_model_cleanup import CleanMixin, ExtensibleValidationError


class SomeModel(CleanMixin, models.Model):
    lorem = models.CharField(max_length=10, blank=True)

    def clean_foo(self):
        raise ValidationError('Foo is bad')

    def clean_bar(self):
        raise ExtensibleValidationError({'bar': _('Bar is wrong cause %s > %s!')}, code='bar', params=(2, 1))

    def clean_legacy(self):
        # We can't init ValidationError as one-liner, cause dict + params are not compatible
        # We need to wrap a message in ValidationError and put that in dict indicating a field
        msg = _('Bar legacy error %s > %s!')
        error = ValidationError(msg, code='bar', params=(7, 5))
        raise ValidationError({'bar': error})

    # This is not longer required:
    def legacy_clean(self):
        errors = []
        try:
            self.clean_foo()
        except ValidationError as ex:
            errors.append(ex)
        errors = []
        try:
            self.clean_bar()
        except ValidationError as ex:
            errors.append(ex)
        errors = []
        try:
            self.clean_legacy()
        except ValidationError as ex:
            errors.append(ex)
        if errors:
            raise ValidationError(errors)
