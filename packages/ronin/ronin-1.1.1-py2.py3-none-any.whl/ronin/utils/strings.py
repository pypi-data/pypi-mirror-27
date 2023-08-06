# -*- coding: utf-8 -*-
#
# Copyright 2016-2018 Tal Liron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .compat import to_unicode
from ..contexts import current_context
import re


_ENCODING = 'utf-8'

UNESCAPED_STRING_RE = re.compile(r'(?<!\\) ')


def stringify(value):
    """
    Casts the value to a Unicode string. If the value is a function, calls it using
    :func:`ronin.contexts.current_context` as its only argument, and recurses until a
    non-FunctionType value is returned.
    
    None values are preserved, whether None is directly sent to this function or is the return
    value of function argument.
    
    This function is the heart of Rōnin's deferred value capability, as it allows lambdas to be
    passed around instead of strings.
    
    :param value: value or None
    :type value: basestring|FunctionType
    :returns: stringified value or None
    :rtype: basestring
    """
    
    if value is None:
        return None
    elif hasattr(value, '__call__'):
        with current_context() as ctx:
            value = value(ctx)
        return stringify(value)
    else:
        try:
            return to_unicode(value)
        except UnicodeDecodeError:
            return str(value).decode(_ENCODING)


def stringify_list(values):
    """
    Calls :func:`stringify` on all elements. Return values of None are preserved.
    
    :param values: values
    :type values: []
    :returns: values
    :rtype: [basestring]
    """
    
    return [stringify(v) for v in values]


def stringify_dict(values):
    """
    Calls :func:`stringify` on all dict values. Return values of None are preserved.
    
    :param values: values
    :type values: {}
    :returns: values
    :rtype: {object: basestring}
    """
    
    return {k: stringify(v) for k, v in values.items()}


def bool_stringify(value):
    """
    Like :func:`stringify`, except checks if the return value equals, ignoring case, to ``true``. 
    
    :param value: value
    :type value: basestring|FunctionType
    :returns: True if the stringified value is ``true``
    :rtype: bool
    """
    
    if value is None:
        return False
    elif hasattr(value, '__call__'):
        with current_context() as ctx:
            value = value(ctx)
        return bool_stringify(value)
    else:
        if isinstance(value, bool):
            return value
        try:
            value = to_unicode(value)
        except UnicodeDecodeError:
            value = str(value).decode(_ENCODING)
        return value.lower() == 'true'


def join_later(values, separator=' '):
    """
    Creates a lambda that calls :func:`stringify_list` and joins the results on ``separator``.
    
    :param values: values
    :type values: []
    :param separator: separator
    :type separator: basestring|FunctionType
    :returns: lambda returning the joined string
    :rtype: FunctionType
    """
    
    return lambda _: stringify(separator).join(stringify_list(values))


def format_later(the_format, *args, **kwargs):
    """
    Creates a lambda that calls :func:`stringify_list` and :func:`stringify_dict` on the arguments
    and then ``.format`` their results on ``the_format``.
    
    :param the_format: format string
    :type the_format: basestring|FunctionType
    :param values: values
    :type values: []
    :returns: lambda returning the formatted string
    :rtype: FunctionType
    """
    
    return lambda _: stringify(the_format).format(*stringify_list(args), **stringify_dict(kwargs)) 
