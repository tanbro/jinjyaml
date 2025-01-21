from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from yaml.nodes import Node, ScalarNode

from .data import Data

if TYPE_CHECKING:  # pragma: no cover
    from yaml.cyaml import _CLoader
    from yaml.loader import _Loader


__all__ = ["Constructor"]


class Constructor:
    """Constructor class for :class:`jinja2.Template` YAML tags.

    When parsing a YAML string, this class constructs template tags into :class:`.Data` objects.

    To add the constructor to a PyYAML loader, use the following code::

        import yaml
        import jinjyaml as jy

        ctor = jy.Constructor()

        # Note: Tag names start with "!"

        # Add to default loader
        yaml.add_constructor("!j2", ctor)
        # or: Add to CLoader
        yaml.add_constructor("!j2", ctor, yaml.CLoader)
        # or: Add to SafeLoader
        yaml.add_constructor("!j2", ctor, yaml.SafeLoader)
        # or: Add to other loaders...

    Attention:
       - Custom YAML tags must start with ``"!"``.
         When invoking ``yaml.add_constructor``,
         the ``tag`` parameter **must** include a single leading ``"!"``.
       - The content of the tag **must** be text.
    """

    def __call__(self, loader: Union[_Loader, _CLoader], node: Node) -> Union[Data, Any]:
        if not isinstance(node, ScalarNode):
            raise TypeError(f"`{self.__class__.__name__}` expects `{ScalarNode.__name__}`, but actual `{type(node).__name__}`")
        source = loader.construct_scalar(node)
        if not isinstance(source, str):  # pragma: no cover
            raise TypeError(f"`{self.__class__.__name__}` expects `str`, but actual `{type(source).__name__}`")
        return Data(source)
