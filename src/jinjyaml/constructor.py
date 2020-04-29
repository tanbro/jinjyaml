from typing import Any, Dict, Optional

import jinja2
import yaml

from .tagobject import JinjyamlObject


class JinjaConstructor:
    """Constructor for template tags

    When loading YAML from string, the class constructs template tag text into :class:`JinjyamlObject` object
    """

    def __init__(self,
                 env: jinja2.Environment = None,
                 auto_render: bool = False,
                 context: Dict[str, Any] = None
                 ):
        """
        :param env: When loading YAML string, :class:`JinjyamlObject` objects will be created for each template tag.

            - if `env` is not `None`:

              it's :attr:`JinjyamlObject.template` data member is constructed by :meth:`jinja2.Environment.from_string`

            - else:

                it's :attr:`JinjyamlObject.template` data member is directly constructed by :class:`jinja2.Template`

        :type env: jinja2.Environment

        :param bool auto_render: render template into objects on loading
        :param context: variables name-value pairs for rendering
        :type context: Dict[str, Any]
        """
        self._env = env
        self._auto_render = auto_render
        self._context = context or {}

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
                '`{}` does not support `{}` YAML node'.format(
                    self.__class__.__name__, type(node))
            )
        tag_obj = JinjyamlObject(source, self._env)
        if self._auto_render:
            return tag_obj.render(loader)
        else:
            return tag_obj
