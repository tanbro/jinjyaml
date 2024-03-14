"""
Application specific tag of Jinja2 template in PyYAML.

It may be useful if you only want to render special tag nodes in the document, instead of whole YAML string as a template.
"""  # noqa: E501

from .constructor import *  # noqa: F403
from .data import *  # noqa: F403
from .functions import *  # noqa: F403
from .representer import *  # noqa: F403
from .version import __version__, __version_tuple__
