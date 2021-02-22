from yaml.nodes import ScalarNode

from .data import Data

__all__ = ['Constructor']


class Constructor:
    """Constructor class for `Jinja2` template YAML tags.

    When parsing YAML string, the class constructs template tags to :class:`.Data` objects.

    Add the constructor to `PyYAML Loader` as below::


        import yaml
        import jinjyaml

        constructor = jinjyaml.Constructor()

        # Attention: tag name starts with "!"
        yaml.add_constructor('!j2', constructor)  
        # or
        yaml.add_constructor('!j2', constructor, yaml.CLoader)


    .. attention::

        - Custom YAML tags start with ``"!"``.

          So, when we call ``yaml.add_constructor``,
          the ``tag`` parameter **MUST** have a single ``"!"`` at the begining.

        - Content of the tag **MUST** be text
    """

    def __call__(self, loader, node):
        if isinstance(node, ScalarNode):
            source = loader.construct_scalar(node)
            if not isinstance(source, str):
                raise TypeError(
                    '`{}` expects `str`, but actual `{}`'.format(
                        self.__class__.__name__, type(source))
                )
        else:
            raise TypeError(
                '`{}` does not support `{}`'.format(
                    self.__class__.__name__, type(node))
            )
        return Data(source, type(loader))
