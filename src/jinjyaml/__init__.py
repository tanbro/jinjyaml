"""
`jinjyaml` provides Jinja2 template custom tag in YAML

it does not render a whole YAML document,
it only render Jinja2 template tag object inside a YAML document.
"""

from .constructor import JinjaConstructor
from .helpers import render_object
from .representer import JinjayamlRepresenter
from .tagobject import JinjyamlObject
from .version import version as __version__
