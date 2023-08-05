#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @namespace pyhttpstatus_utils
"""
HTTP Status Codes and Support Functions.
"""

import copy

from .status_dicts import name as http_status_codes
from .status_dicts import description as http_status_desc
from .status_dicts import type as http_status_types
from .status_type import HttpStatusType


class InvalidHttpCode(Exception):
    pass


def validate_http_code(http_code, minimum=100, maximum=599, strict=True, default_http_code=0):
    """Validate HTTP code. If strict, throw, else just return default_http_code."""
    try:
        http_code = int(http_code)
    except:
        if strict:
            raise InvalidHttpCode('[{}] {}  is not a valid integer'.format(http_code, type(http_code)))
        else:
            return default_http_code

    if http_code < minimum:
        if strict:
            raise InvalidHttpCode('{} is below minimum HTTP status code {}'.format(http_code, minimum))
        else:
            return default_http_code
    elif http_code > maximum:
        if strict:
            raise InvalidHttpCode('{} is above maximum HTTP status code {}'.format(http_code, maximum))
        else:
            return default_http_code
    return http_code


def http_status_dict(override_dict=None):
    """HTTP Status Dictionary with Overrides if provided.

    Args:
        override_dict:

    Returns:

    """
    dict_ = copy.deepcopy(http_status_codes)

    if override_dict and isinstance(override_dict, dict) and len(override_dict) > 0:
        for key, value in override_dict.items():
            if key in dict_:
                http_status = dict_[key].rstrip('\.')
                dict_[key] = "{}: {}".format(http_status, value).rstrip('\.') + '.'
            else:
                dict_.update({key: value})

    return dict_


def http_status_code_to_desc(http_status_code):
    """Get HTTP status code description.

    Args:
        http_status_code:

    Returns:

    """
    validate_http_code(http_status_code)
    if http_status_code not in http_status_codes:
        return http_status_code_to_type(http_status_code)

    return http_status_desc[http_status_code]


def http_status_code_to_type(http_status_code):
    """Get HTTP Status Code Type

    Args:
        http_status_code:

    Returns:

    """
    validate_http_code(http_status_code)
    http_status_code_base = int(http_status_code / 100) * 100

    return http_status_types[http_status_code_base]


def is_http_status_type(http_status_code, http_status_type):
    """Match if provided HTTP Status Code is expected
    HTTP Status Code Type.

    Args:
        http_status_code:
        http_status_type:

    Returns:

    """
    return http_status_code_to_type(http_status_code) == http_status_type


def is_http_status_successful(http_status_code):
    """Check if HTTP Status Code is type Successful

    Args:
        http_status_code:
        logger:

    Returns:

    """
    return is_http_status_type(http_status_code=http_status_code, http_status_type=HttpStatusType.SUCCESSFUL)
