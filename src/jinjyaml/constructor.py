from typing import Any, Dict

import jinja2
import yaml

from .tagobject import JinjyamlObject

__all__ = ['JinjyamlConstructor']


class JinjyamlConstructor:
    """Constructor for template tags

    When loading an object from YAML string, the class constructs template tag text into :class:`.JinjyamlObject` object

    Add the constructor into YAML's loader class as::

        constructor = JinjyamlConstructor()
        yaml.add_constructor('!jinja2', constructor)  # "!" here!!!

    .. attention::

        - custom tags in YAML should start with ``"!"``
        - when invoking ``yaml.add_constructor``, the ``tag`` parameter should start with ``"!"``
        - content of the tag **MUST be a text scalar node** in YAML
    """

    def __init__(self,
                 env: jinja2.Environment = None,
                 auto_render: bool = False,
                 context: Dict[str, Any] = None
                 ):
        """
        :param jinja2.Environment env:
            When loading YAML string, :class:`.JinjyamlObject` objects will be constructed for each template tag.

            And it's :attr:`.JinjyamlObject.template` data member is created by:

            - :class:`jinja2.Template`'s constructor function directly, if ``env`` parameter is ``None``
            - :meth:`jinja2.Environment.from_string`, if ``env`` parameter is not ``None``

        :param bool auto_render: whether to render template into an object on loading

        :param context: variables name-value pairs for :mod:`jinja2` template rendering
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
            return tag_obj.render(type(loader), self._context)
        else:
            return tag_obj
