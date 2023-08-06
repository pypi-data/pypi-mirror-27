# -*- coding: utf-8 -*-
"""zhao.xin_re
This module provides common re.
"""
import re

IPV4_SRE = re.compile(
    r'((?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})')
