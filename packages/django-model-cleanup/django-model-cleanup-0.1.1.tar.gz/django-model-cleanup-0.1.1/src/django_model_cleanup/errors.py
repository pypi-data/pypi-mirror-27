# coding=utf-8
from __future__ import unicode_literals

from collections import OrderedDict

import six
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.utils.encoding import force_text


class ExtensibleValidationError(ValidationError):
    def __init__(self, message, code=None, params=None):
        """
        The `message` argument can be a single error, a list of errors, or a
        dictionary that maps field names to lists of errors. What we define as
        an "error" can be either a simple string or an instance of
        ValidationError with its message attribute set, and what we define as
        list or dictionary can be an actual `list` or `dict` or an instance
        of ValidationError with its `error_list` or `error_dict` attribute set.
        """

        # PY2 can't pickle naive exception: http://bugs.python.org/issue1692335.
        super(ValidationError, self).__init__(message, code, params)

        if isinstance(message, ValidationError):
            if hasattr(message, 'error_dict'):
                message = message.error_dict
            # PY2 has a `message` property which is always there so we can't
            # duck-type on it. It was introduced in Python 2.5 and already
            # deprecated in Python 2.6.
            elif not hasattr(message, 'message' if six.PY3 else 'code'):
                message = message.error_list
            else:
                message, code, params = message.message, message.code, message.params

        if isinstance(message, dict):
            self.error_dict = {}
            for field, messages in message.items():
                if not isinstance(messages, ExtensibleValidationError):
                    # Let's pass on code and params along with messages from dict
                    messages = ExtensibleValidationError(messages, code, params)
                self.error_dict[field] = messages.error_list

        elif isinstance(message, list):
            self.error_list = []
            for item in message:
                if not isinstance(item, ExtensibleValidationError):
                    # Normalize plain strings to instances of ValidationError.
                    item = ExtensibleValidationError(item, code, params)
                if hasattr(item, 'error_dict') and hasattr(self, 'error_list'):
                    # Convert self from list to dict and prepare for dict update later on
                    self.error_dict = OrderedDict()
                    if self.error_list:
                        self.error_dict[NON_FIELD_ERRORS] = self.error_list
                    del self.error_list
                if hasattr(self, 'error_list'):
                    # Extend error_list with passed in item.error_list
                    self.error_list.extend(item.error_list)
                elif hasattr(item, 'error_list'):
                    # Extend __all__ errors with passed in item.error_list
                    self.error_dict.setdefault(NON_FIELD_ERRORS, []).extend(item.error_list)
                else:
                    # Concat error dictionaries
                    for field, errors in item.error_dict.items():
                        self.error_dict.setdefault(field, []).extend(errors)
        else:
            self.message = message
            self.code = code
            self.params = params
            self.error_list = [self]

    @property
    def messages(self):
        if hasattr(self, 'error_dict'):
            return sum(OrderedDict(self).values(), [])
        return list(self)

    def __iter__(self):
        if hasattr(self, 'error_dict'):
            for field, errors in self.error_dict.items():
                yield field, list(ValidationError(errors))
        else:
            for error in self.error_list:
                message = error.message
                if error.params:
                    message %= error.params
                yield force_text(message)
