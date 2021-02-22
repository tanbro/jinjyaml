"""
``jinjyaml`` provides custom ``Jinja2`` template tags for ``PyYAML``.

It does not render whole YAML document,
it only renders Jinja2 template tag objects inside a YAML document.
"""

from .constructor import *
from .data import *
from .functions import *
from .representer import *
from .version import version as __version__
