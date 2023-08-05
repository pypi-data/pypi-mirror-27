# {# pkglts, version
#  -*- coding: utf-8 -*-

major = {{ version.major }}
"""(int) Version major component."""

minor = {{ version.minor }}
"""(int) Version minor component."""

post = {{ version.post }}
"""(int) Version post or bugfix component."""

__version__ = ".".join([str(s) for s in (major, minor, post)])
# #}
