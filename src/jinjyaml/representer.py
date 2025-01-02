from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from yaml import Dumper, ScalarNode

from .data import Data

__all__ = ["Representer"]


@dataclass
class Representer:
    """Representer for :class:`jinja2.Template` tags.

    When dumping an object into a YAML string, this class converts :class:`.Data` objects to their string representation.

    To add the representer to a PyYAML dumper, use the following code::

        representer = jinjyaml.Representer("j2")  # Note: No "!" here!
        yaml.add_representer(Node, representer)

    Attention:
        - The tag name passed to the `Representer` constructor **MUST NOT** include the leading "!".
          This is because PyYAML automatically adds the "!" when registering the representer.
        - Ensure that `Node` is the correct type for the objects you want to represent.
    """

    tag: str
    """YAML tag name for include statement

    Attention:
        Custom YAML tag's name starts with ``"!"``.
        But we **MUST NOT** put a ``"!"`` at the beginning here,
        because :func:`yaml.add_representer` will add the symbol itself.
    """

    def __call__(self, dumper: Dumper, data: Data) -> ScalarNode:
        if not isinstance(data, Data):
            raise TypeError(f"{type(data)}")
        return dumper.represent_scalar(f"!{self.tag}", data.source)
