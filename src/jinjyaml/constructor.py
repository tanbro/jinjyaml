from yaml.nodes import ScalarNode

from .data import Data

__all__ = ["Constructor"]


class Constructor:
    """Constructor class for :class:`jinja2.Template` YAML tags.

    When parsing YAML string, the class constructs template tags to :class:`.Data` objects.

    Add the constructor to `PyYAML Loader` as below::


        import yaml
        import jinjyaml as jy

        ctor = jy.Constructor()

        # Attention: tag name starts with "!"

        # Add to default loader
        yaml.add_constructor("!j2", ctor)
        # or: Add to CLoader
        yaml.add_constructor("!j2", ctor, yaml.CLoader)
        # or: Add to SafeLoader
        yaml.add_constructor("!j2", ctor, yaml.SafeLoader)
        # or: Add to other Loaders ...

    Attention:
       - Custom YAML tag starts with ``"!"``.
         When we invoke ``yaml.add_constructor``,
         the ``tag`` parameter **MUST** have a single ``"!"`` at the beginning.
       - Content of the tag **MUST** be text
    """  # noqa: E501

    def __call__(self, loader, node):
        if isinstance(node, ScalarNode):
            source = loader.construct_scalar(node)
            if not isinstance(source, str):  # pragma: no cover
                raise ValueError("`{}` expects `str`, but actual `{}`".format(self.__class__, type(source)))
        else:
            raise TypeError("`{}` does not support `{}` node".format(self.__class__, type(node)))
        return Data(source)
