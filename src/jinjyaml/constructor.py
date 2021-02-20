from typing import Any, Dict, Optional

import jinja2
import yaml

from .data import Data

__all__ = ['Constructor']


class Constructor:
    """Constructor for `Jinja2` template tags

    When parsing YAML string, the class constructs template tag text into :class:`.Data` object

    Add the constructor to `PyYAML Loader` as below::

        constructor = jinjyaml.Constructor()
        yaml.add_constructor('!j2', constructor)  # "!" here!!!

    .. attention::

        - Custom tags in YAML starts by ``"!"``.

          When call ``yaml.add_constructor``,
          the ``tag`` parameter **MUST** have a single ``"!"`` at the first position.

        - Content of the tag **MUST** be text
    """

    def __init__(self,
                 env: Optional[jinja2.Environment] = None,
                 auto_extract: Optional[bool] = False,
                 context: Optional[Dict[str, Any]] = None
                 ):
        """
        :param jinja2.Environment env:
            A :class:`.Data` object is created for each template tag When parsing YAML.

            And it's :attr:`.Data.template` data member is created by:

            - :class:`jinja2.Template`'s constructor function directly, if ``env`` parameter is ``None``
            - :meth:`jinja2.Environment.from_string`, if ``env`` parameter is instance of :class:`jinja2.Environment`

        :param bool auto_extract:
            Whether to render template and parse it when loading.

        :type context: Dict[str, Any]
        :param context:
            Variables name-value pairs for :mod:`jinja2` template rendering.
        """
        self._env = env
        self._auto_extract = auto_extract
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
        data = Data(source, self._env)
        if self._auto_extract:
            return data.extract(type(loader), self._context)
        else:
            return data
