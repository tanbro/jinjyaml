"""
Constructor class for Jinja Template YAML tag
"""

import jinja2
import yaml

from .tagobject import JinjyamlObject


class JinjaConstructor:
    def __init__(self, env=None, auto_render=False, context=None):
        """
        :param jinja2.Environment env:
        :param bool auto_render:
        :param dict context:
        """
        self._env = env
        self._auto_render = auto_render
        self._context = context or {}

    def _make_template(self, source):
        if self._env:
            return self._env.from_string(source)
        else:
            return jinja2.Template(source)

    def __call__(self, loader, node):
        if isinstance(node, yaml.nodes.ScalarNode):
            args = [loader.construct_scalar(node)]
            source = args[0]
            if not isinstance(source, str):
                raise TypeError(
                    '`{}` expects `str`, but actual `{}`'.format(
                        self.__class__.__name__, type(source))
                )
        else:
            raise TypeError(
                '`{}` does not support node type `{}`'.format(
                    self.__class__.__name__, type(node))
            )
        tag_obj = JinjyamlObject(source, self._env)
        if self._auto_render:
            return tag_obj.render(loader)
        else:
            return tag_obj
