"""
Application specific tag of Jinja2 template in PyYAML.

It may be useful if you only want to render special tag nodes in the document,
instead of whole YAML string as a template.
"""

# ruff: noqa: F401

from .constructor import Constructor
from .data import Data
from .functions import extract
from .representer import Representer
from .version import __version__, __version_tuple__
