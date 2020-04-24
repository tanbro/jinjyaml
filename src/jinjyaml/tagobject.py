from typing import Dict, Any

import jinja2
import yaml

from .utils import JinjaTemplateGenerateStreamReader


class JinjyamlObject:
    def __init__(self, source: str, env: jinja2.Environment = None):
        self._source = source
        self._env = env
        self._template = None

    @property
    def source(self) -> str:
        return self._source

    @property
    def template(self) -> jinja2.Template:
        if self._template is None:
            if self._env:
                self._template = self._env.from_string(self.source)
            else:
                self._template = jinja2.Template(self.source)
        return self._template

    def render(self, loader_class=None, context: Dict[str, Any] = None):
        if context is None:
            context = dict()
        stream = JinjaTemplateGenerateStreamReader(self.template.generate(**context))
        obj = yaml.load(stream, loader_class)
        return obj
