"""
`jinjyaml` provides Jinja2 template custom tag in YAML

it does not render a whole YAML document,
it only render Jinja2 template tag object inside a YAML document.
"""

from .constructor import *
from .helpers import *
from .representer import *
from .tagobject import *
from .version import version as __version__
