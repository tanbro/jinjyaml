from typing import Any, Dict, Optional, Type, Union

import jinja2
import yaml

from .types import TJson

__all__ = ['JinjyamlObject']


class JinjyamlObject:
    """Template YAML tag object
    """

    def __init__(self, source: str, env: Optional[jinja2.Environment] = None):
        self._env = env
        self._source = source
        self._template = None

    @property
    def source(self) -> str:
        """Source code to make :attr:`template`

        :rtype: str
        """
        return self._source

    @property
    def template(self) -> jinja2.Template:
        """Template object made from :attr:`source`

        :rtype: jinja2.Template
        """
        if self._template is None:
            if self._env:
                self._template = self._env.from_string(self._source)
            else:
                self._template = jinja2.Template(self._source)
        return self._template

    def extract(self,
                loader_class: Optional[Type] = None,
                context: Optional[Dict[str, Any]] = None
                ) -> TJson:
        """Do rendering, then parse it using a `PyYAML Loader`.

        :param loader_class:
            `PyYAML Loader` class to parse the rendered string.

        :type context: Dict[str, Any]
        :param context:
            Variables name-value pairs for template rendering.

        :return: Parsed object
        """
        if context is None:
            context = dict()
        txt = self.template.render(**context)
        obj = yaml.load(txt, loader_class)
        return obj


TLoadedObject = Union[TJson, JinjyamlObject]
