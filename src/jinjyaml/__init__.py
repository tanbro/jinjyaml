"""
Application specific tag of Jinja2 template in PyYAML.

It may be useful if you only want to render special tag nodes in the document,
instead of whole YAML string as a template.
"""

from .constructor import *
from .data import *
from .functions import *
from .representer import *
from .version import version as __version__
