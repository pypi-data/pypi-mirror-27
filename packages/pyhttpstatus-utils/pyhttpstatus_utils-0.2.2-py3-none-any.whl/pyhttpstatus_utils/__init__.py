#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @namespace pyhttpstatus_utils

__title__ = 'pyhttpstatus-utils'
__version__ = '0.2.2'
__version_info__ = tuple(__version__.split('.'))

__author__ = 'jefft@tune.com'
__license__ = 'MIT License'

__python_required_version__ = (3, 0)

from .status_dicts import name as http_status_codes
from .status_dicts import description as http_status_desc
from .status_dicts import type as http_status_types
from .status_code import HttpStatusCode
from .status_type import HttpStatusType

from .status_methods import (
    http_status_dict,
    http_status_code_to_desc,
    http_status_code_to_type,
    is_http_status_type,
    is_http_status_successful,
    validate_http_code
)
